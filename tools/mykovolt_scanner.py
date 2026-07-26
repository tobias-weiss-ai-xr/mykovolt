#!/usr/bin/env python3
"""
MykoVolt Scanner — NFC Data Reader & Analyzer

Reads soil moisture data from MykoVolt DevKit NFC tags.
Works with any NFC reader via libnfc or PCSC, plus simulation mode.

Usage:
    mykovolt scan                     # Scan for nearby MykoVolt tags
    mykovolt read                     # Read all data from a tag
    mykovolt export --csv output.csv  # Export data to CSV
    mykovolt status                   # Show tag status (battery, entries)
    mykovolt simulate --days 7        # Generate simulated data for testing
    mykovolt analyze --days 7         # Analyze moisture trends from exported data

Protocol:
    MykoVolt tags use ISO 15693 (ST25DV04K).
    MCU writes 16-byte entries to NTAG EEPROM via I²C.
    Phone reads EEPROM blocks over NFC using READ_BLOCK commands.

Data format (16-byte entry):
    Offset  Size  Type    Field
    0       4     uint32  timestamp (Unix seconds, RTC-based)
    4       2     int16   capacitance (0.01 pF resolution, ±327.68 pF)
    6       2     uint16  v_batt (pressling voltage in mV)
    8       2     int16   temperature (0.1 °C resolution)
    10      2     uint16  adc_aux (auxiliary channel)
    12      1     uint8   flags (error, cal, low_batt, overflow)
    13      1     uint8   crc_lo (XOR of all bytes)
    14      2     —       reserved
"""

import argparse
import json
import csv
import sys
import os
import struct
import time
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List, Optional, Dict
import math

# ──────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────

I2C_ADDRESS_NFC = 0x53
EEPROM_SIZE = 4096  # ST25DV04K: 4 KB
BLOCK_SIZE = 4      # 4 bytes per EEPROM block
ENTRY_SIZE = 16     # 16 bytes per measurement entry
HEADER_SIZE = 256   # First 256 bytes = system header
RING_BUFFER_START = 256
MAX_ENTRIES = (EEPROM_SIZE - HEADER_SIZE) // ENTRY_SIZE  # 240 entries

# Flags
FLAG_ERROR = 0x01
FLAG_CALIBRATION = 0x02
FLAG_LOW_BATTERY = 0x04
FLAG_OVERFLOW = 0x08

FLAG_NAMES = {
    FLAG_ERROR: "ERROR",
    FLAG_CALIBRATION: "CAL",
    FLAG_LOW_BATTERY: "LOW_BATT",
    FLAG_OVERFLOW: "OVERFLOW",
}

# ──────────────────────────────────────────────
# Data Model
# ──────────────────────────────────────────────

@dataclass
class Measurement:
    """Single soil moisture measurement."""
    timestamp: float          # Unix timestamp
    capacitance_raw: int      # FDC1004 raw count
    capacitance_pf: float     # Converted to pF
    v_batt_mv: int            # Pressling voltage in mV
    temperature_c: float      # Temperature in °C
    adc_aux: int              # Auxiliary ADC value
    flags: int                # Bitfield flags
    flags_human: List[str]    # Human-readable flags
    crc_ok: bool              # CRC check passed
    index: int                # Entry index in ring buffer


@dataclass
class TagData:
    """Complete data read from a MykoVolt tag."""
    magic: bytes               # 4-byte magic "MVLT"
    version: int               # Firmware version
    write_pointer: int         # Current write position
    config: int                # Configuration flags
    interval_min: int          # Measurement interval in minutes
    v_batt_now: int            # Current pressling voltage
    entries: List[Measurement] # Measurement entries
    total_entries: int         # Total valid entries
    first_ts: Optional[float]  # First measurement timestamp
    last_ts: Optional[float]   # Last measurement timestamp
    
    @property
    def duration_hours(self) -> float:
        """Duration covered by measurements in hours."""
        if self.first_ts and self.last_ts:
            return (self.last_ts - self.first_ts) / 3600
        return 0.0
    
    @property
    def avg_temperature(self) -> Optional[float]:
        """Average temperature in °C."""
        if self.entries:
            return sum(e.temperature_c for e in self.entries) / len(self.entries)
        return None
    
    @property
    def avg_capacitance(self) -> Optional[float]:
        """Average capacitance in pF."""
        if self.entries:
            return sum(e.capacitance_pf for e in self.entries) / len(self.entries)
        return None


# ──────────────────────────────────────────────
# Data Parsing
# ──────────────────────────────────────────────

def capacitance_raw_to_pf(raw: int) -> float:
    """Convert stored int16 (0.01 pF resolution) to capacitance in pF."""
    # Handle unsigned interpretation if stored as uint16 accidentally
    if raw > 32767:
        raw = raw - 65536
    return raw / 100.0


def vwc_from_capacitance(cap_pf: float, dry_cap: float = 0.5, wet_cap: float = 3.2) -> float:
    """Estimate Volumetric Water Content from capacitance.
    Linear mapping between dry (0%) and wet (100%) capacitance.
    """
    if cap_pf <= dry_cap:
        return 0.0
    if cap_pf >= wet_cap:
        return 100.0
    return (cap_pf - dry_cap) / (wet_cap - dry_cap) * 100.0


def parse_entry(data: bytes, index: int) -> Optional[Measurement]:
    """Parse a 16-byte measurement entry."""
    if len(data) < ENTRY_SIZE:
        return None
    
    ts = struct.unpack_from('<I', data, 0)[0]          # uint32 timestamp
    cap_raw = struct.unpack_from('<H', data, 4)[0]     # uint16 capacitance
    v_batt = struct.unpack_from('<H', data, 6)[0]      # uint16 voltage
    temp_raw = struct.unpack_from('<H', data, 8)[0]    # uint16 temperature
    adc = struct.unpack_from('<H', data, 10)[0]        # uint16 aux
    flags = data[12]                                    # uint8 flags
    crc_byte = data[13]                                 # uint8 CRC
    
    # Parse temperature (0.1°C resolution, signed int16)
    if temp_raw > 32767:
        temp_raw = temp_raw - 65536
    temp_c = temp_raw / 10.0
    
    # Simple CRC check (XOR of all bytes except CRC byte)
    calc_crc = 0
    for i in range(ENTRY_SIZE):
        if i != 13:  # Skip CRC byte
            calc_crc ^= data[i]
    crc_ok = (calc_crc & 0xFF) == crc_byte
    
    # Parse flags
    flag_list = [name for mask, name in FLAG_NAMES.items() if flags & mask]
    
    cap_pf = capacitance_raw_to_pf(cap_raw)
    
    return Measurement(
        timestamp=ts,
        capacitance_raw=cap_raw,
        capacitance_pf=round(cap_pf, 3),
        v_batt_mv=v_batt * 3,  # Voltage divider: ADC reads Vbatt/3
        temperature_c=round(temp_c, 1),
        adc_aux=adc,
        flags=flags,
        flags_human=flag_list,
        crc_ok=crc_ok,
        index=index
    )


def parse_tag_data(eeprom_data: bytes) -> TagData:
    """Parse complete EEPROM contents from a MykoVolt tag."""
    if len(eeprom_data) < HEADER_SIZE + ENTRY_SIZE:
        raise ValueError(f"Data too short: {len(eeprom_data)} bytes (need {HEADER_SIZE + ENTRY_SIZE})")
    
    # Parse header (first 256 bytes)
    magic = eeprom_data[0:4]
    version = eeprom_data[4]
    write_ptr = struct.unpack_from('<H', eeprom_data, 8)[0]
    config = struct.unpack_from('<I', eeprom_data, 12)[0]
    interval_min = eeprom_data[16]
    v_batt_now = struct.unpack_from('<H', eeprom_data, 18)[0] * 3
    
    # Sanity check magic
    if magic != b'MVLT':
        print(f"  ⚠️  Unknown magic: {magic} (expected 'MVLT')")
    
    # Parse entries from ring buffer
    entries = []
    total_bytes = len(eeprom_data)
    num_possible = (total_bytes - HEADER_SIZE) // ENTRY_SIZE
    
    for i in range(num_possible):
        offset = HEADER_SIZE + i * ENTRY_SIZE
        chunk = eeprom_data[offset:offset + ENTRY_SIZE]
        
        # Skip empty entries (all zeros)
        if all(b == 0 for b in chunk):
            continue
        
        entry = parse_entry(chunk, i)
        if entry and entry.timestamp > 1700000000:  # Sanity: after 2023
            entries.append(entry)
    
    # Sort by timestamp
    entries.sort(key=lambda e: e.timestamp)
    
    # Determine time range
    first_ts = entries[0].timestamp if entries else None
    last_ts = entries[-1].timestamp if entries else None
    
    return TagData(
        magic=magic,
        version=version,
        write_pointer=write_ptr,
        config=config,
        interval_min=interval_min,
        v_batt_now=v_batt_now,
        entries=entries,
        total_entries=len(entries),
        first_ts=first_ts,
        last_ts=last_ts
    )


# ──────────────────────────────────────────────
# Simulation (for testing without hardware)
# ──────────────────────────────────────────────

def generate_simulated_data(days: float = 7.0, interval_min: float = 15.0,
                            temp_min: float = 15.0, temp_max: float = 30.0,
                            moisture_daily: float = 0.5) -> bytes:
    """Generate realistic simulated EEPROM data for testing.
    
    Args:
        days: Number of days to simulate
        interval_min: Measurement interval in minutes
        temp_min: Minimum daily temperature (°C)
        temp_max: Maximum daily temperature (°C)
        moisture_daily: Daily watering schedule (0=none, 1=daily)
    
    Returns:
        4096 bytes of simulated EEPROM data
    """
    import numpy as np
    
    eeprom = bytearray(4096)
    
    # Header
    eeprom[0:4] = b'MVLT'
    eeprom[4] = 0x01  # Version 1
    struct.pack_into('<H', eeprom, 8, HEADER_SIZE)  # Write pointer at start
    struct.pack_into('<I', eeprom, 12, 0)           # Config
    eeprom[16] = int(interval_min)                   # Interval
    struct.pack_into('<H', eeprom, 18, 450)          # Vbatt (450 mV * 3 = 1350 mV reading)
    
    # Generate entries
    n_entries = int(days * 24 * 60 / interval_min)
    base_ts = int(time.time()) - int(days * 86400)
    rng = np.random.default_rng(42)
    
    for i in range(min(n_entries, MAX_ENTRIES)):
        ts = base_ts + int(i * interval_min * 60)
        
        # Temperature: sine wave with daily cycle
        hour = (i * interval_min / 60) % 24
        temp = temp_min + (temp_max - temp_min) * 0.5 * (1 + math.sin(2 * math.pi * hour / 24 - math.pi / 2))
        temp += rng.normal(0, 0.5)  # noise
        
        # Capacitance: base 0.5 pF (dry) + water events + noise
        cap_base = 0.5
        # Watering events: every 1-3 days, add moisture
        days_since_start = i * interval_min / (24 * 60)
        water_events = int(days_since_start // (1.0 + rng.random() * 2))
        cap_extra = 0
        for w in range(water_events):
            # Each watering adds 0.3-1.0 pF that decays exponentially
            hours_since_water = days_since_start * 24 - (w + 0.5) * (24 + rng.random() * 48)
            if hours_since_water > 0:
                cap_extra += 0.8 * math.exp(-hours_since_water / 48) * (0.5 + rng.random())
        cap_pf = cap_base + cap_extra + rng.normal(0, 0.02)
        cap_pf = max(0.1, min(4.0, cap_pf))
        
        # Convert capacitance to raw int16 (0.01 pF resolution)
        cap_raw = int(cap_pf * 100)
        cap_raw = max(-32768, min(32767, cap_raw))
        
        # Voltage: slowly declining
        v_batt = int((450 - days_since_start * 3 + rng.normal(0, 5)) / 3)
        v_batt = max(100, min(500, v_batt))
        
        # Temperature raw (0.1°C resolution)
        temp_raw = int(max(-100, min(600, temp * 10)))
        
        # Aux ADC (soil moisture second channel, correlated)
        aux_raw = int(cap_pf * 5000 + rng.normal(0, 50))
        
        # Flags
        flags = 0
        if cap_pf > 3.5: flags |= FLAG_OVERFLOW
        if v_batt < 100: flags |= FLAG_LOW_BATTERY
        
        # Build entry
        entry = bytearray(16)
        struct.pack_into('<I', entry, 0, ts)
        struct.pack_into('<H', entry, 4, cap_raw & 0xFFFF)
        struct.pack_into('<H', entry, 6, v_batt & 0xFFFF)
        struct.pack_into('<H', entry, 8, temp_raw & 0xFFFF)
        struct.pack_into('<H', entry, 10, aux_raw & 0xFFFF)
        entry[12] = flags
        
        # CRC (XOR of all bytes except CRC position)
        crc = 0
        for j in range(16):
            if j != 13:
                crc ^= entry[j]
        entry[13] = crc & 0xFF
        
        # Write to ring buffer
        offset = HEADER_SIZE + (i % MAX_ENTRIES) * ENTRY_SIZE
        eeprom[offset:offset + ENTRY_SIZE] = entry
    
    return bytes(eeprom)


# ──────────────────────────────────────────────
# Output Formatters
# ──────────────────────────────────────────────

def format_tag_header(data: TagData):
    """Print tag header summary."""
    print(f"\n  {'='*50}")
    print(f"  MykoVolt DevKit — Tag Readout")
    print(f"  {'='*50}")
    if data.magic == b'MVLT':
        print(f"  ✅ Magic:         {data.magic.decode()} (verified)")
    else:
        print(f"  ⚠️  Magic:         {data.magic}")
    print(f"  Firmware:       v{data.version}")
    print(f"  Write pointer:  {data.write_pointer}")
    print(f"  Interval:       {data.interval_min} min")
    print(f"  Vbatt now:      {data.v_batt_now} mV")
    print(f"  {'='*50}")


def format_entries(entries: List[Measurement], verbose: bool = False):
    """Print measurement entries."""
    if not entries:
        print("  No entries found.")
        return
    
    print(f"  {'Idx':>4} {'Time':<20} {'Cap (pF)':<10} {'VWC (%)':<9} {'Vbatt':<7} {'Temp':<7} {'Flags':<15} {'CRC':>4}")
    print(f"  {'─'*80}")
    
    for e in entries[-20:]:  # Show last 20
        ts_str = datetime.fromtimestamp(e.timestamp).strftime('%Y-%m-%d %H:%M')
        vwc = vwc_from_capacitance(e.capacitance_pf)
        flags_str = ','.join(e.flags_human) if e.flags_human else 'OK'
        crc_str = '✓' if e.crc_ok else '✗'
        print(f"  {e.index:4d} {ts_str:20s} {e.capacitance_pf:<10.3f} {vwc:<9.1f} {e.v_batt_mv:4d}mV {e.temperature_c:5.1f}°C {flags_str:<15s}  {crc_str:>3s}")
    
    if len(entries) > 20:
        print(f"  ... and {len(entries) - 20} more entries")
    print(f"  Total: {len(entries)} entries")


def output_csv(entries: List[Measurement], path: str):
    """Export entries to CSV file."""
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['index', 'timestamp', 'datetime', 'capacitance_raw', 'capacitance_pF',
                        'vwc_pct', 'v_batt_mV', 'temperature_C', 'adc_aux', 'flags', 'flags_human', 'crc_ok'])
        
        for e in entries:
            vwc = vwc_from_capacitance(e.capacitance_pf)
            ts_str = datetime.fromtimestamp(e.timestamp).strftime('%Y-%m-%d %H:%M:%S')
            flags_str = '|'.join(e.flags_human) if e.flags_human else 'OK'
            writer.writerow([
                e.index, e.timestamp, ts_str, e.capacitance_raw, e.capacitance_pf,
                round(vwc, 1), e.v_batt_mv, e.temperature_c, e.adc_aux,
                e.flags, flags_str, int(e.crc_ok)
            ])
    print(f"  ✅ Exported {len(entries)} entries to {path}")


def analyze_moisture(entries: List[Measurement]):
    """Analyze moisture trends from measurement data."""
    if len(entries) < 2:
        print("  Need at least 2 entries for analysis.")
        return
    
    caps = [e.capacitance_pf for e in entries]
    temps = [e.temperature_c for e in entries]
    voltages = [e.v_batt_mv for e in entries]
    
    min_cap = min(caps)
    max_cap = max(caps)
    avg_cap = sum(caps) / len(caps)
    
    # Estimate dry/wet from data
    dry_vwc = vwc_from_capacitance(min_cap)
    wet_vwc = vwc_from_capacitance(max_cap)
    avg_vwc = vwc_from_capacitance(avg_cap)
    
    # Rate of change
    dur_hours = (entries[-1].timestamp - entries[0].timestamp) / 3600
    cap_rate = (caps[-1] - caps[0]) / dur_hours if dur_hours > 0 else 0
    
    print(f"\n  🌱 MOISTURE ANALYSIS")
    print(f"  {'='*50}")
    print(f"  Period:           {dur_hours:.1f} hours ({dur_hours/24:.1f} days)")
    print(f"  Entries:          {len(entries)}")
    print(f"  Capacitance range: {min_cap:.2f} – {max_cap:.2f} pF")
    print(f"  VWC range:         {dry_vwc:.0f} – {wet_vwc:.0f} %")
    print(f"  Average VWC:       {avg_vwc:.1f} %")
    print(f"  Temperature range: {min(temps):.1f} – {max(temps):.1f} °C")
    print(f"  Voltage range:     {min(voltages)} – {max(voltages)} mV")
    print(f"  Cap change rate:   {cap_rate:+.4f} pF/hour")
    
    # Moisture interpretation
    if avg_vwc < 15:
        print(f"  🏜️  Very dry soil — time to water!")
    elif avg_vwc < 30:
        print(f"  🌿 Good moisture for most plants")
    elif avg_vwc < 60:
        print(f"  🌧️  Moist soil — good for fungi")
    else:
        print(f"  💧 Saturated — drainage issue?")
    
    # Voltage health
    v_avg = sum(voltages) / len(voltages)
    v_trend = (voltages[-1] - voltages[0]) / dur_hours if dur_hours > 0 else 0
    print(f"  Voltage trend:    {v_trend:+.2f} mV/hour")
    if v_avg < 300:
        print(f"  ⚡ LOW VOLTAGE — pressling may be exhausted")
    elif v_avg < 400:
        print(f"  ⚡ Marginal voltage — check pressling health")
    else:
        print(f"  ⚡ Healthy pressling voltage")
    print(f"  {'='*50}\n")


# ──────────────────────────────────────────────
# NFC Reader Interface (stub — real hardware)
# ──────────────────────────────────────────────

class NFCReader:
    """Interface to NFC reader hardware.
    
    Supports:
    - libnfc (most USB NFC readers)
    - PCSC (smart card readers with NFC)
    - Simulated (for testing)
    """
    
    def __init__(self, backend: str = 'simulate'):
        self.backend = backend
        self._connected = False
    
    def connect(self) -> bool:
        """Connect to NFC reader."""
        if self.backend == 'simulate':
            self._connected = True
            return True
        
        print(f"  NFC reader ({self.backend}) — not implemented in this environment")
        print(f"  Use --simulate or run on a machine with libnfc")
        return False
    
    def scan(self) -> List[Dict]:
        """Scan for nearby ISO 15693 tags."""
        if self.backend == 'simulate':
            print("  📡 Simulating tag scan...")
            return [{'uid': 'MVLT-00000001', 'type': 'ST25DV04K', 'rssi': -45}]
        
        print(f"  🔍 Scanning for NFC tags (ISO 15693)...")
        # Real implementation would use libnfc or PCSC
        return []
    
    def read_eeprom(self, uid: str) -> bytes:
        """Read full EEPROM (4 KB) from a MykoVolt tag."""
        if self.backend == 'simulate':
            print(f"  📖 Reading simulated EEPROM...")
            return generate_simulated_data(days=7, interval_min=15)
        
        # Real implementation would send ISO 15693 READ_BLOCK commands
        # 4096 bytes / 4 bytes per block = 1024 blocks
        print(f"  📖 Reading 1024 blocks from tag {uid}...")
        return b''
    
    def close(self):
        self._connected = False


# ──────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='MykoVolt Scanner — NFC Soil Moisture Data Reader',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mykovolt scan                    Scan for tags (simulated)
  mykovolt read --simulate         Read simulated 7-day data
  mykovolt read --from-file tag.bin  Read from saved binary dump
  mykovolt export --csv data.csv   Export to CSV
  mykovolt analyze                 Analyze moisture trends
  mykovolt simulate --days 14      Generate 14 days of test data
  
Protocol: ISO 15693 (ST25DV04K), 4096-byte EEPROM,
          16-byte measurement entries, 240 max.
        """
    )
    
    parser.add_argument('command', nargs='?', default='scan',
                       choices=['scan', 'read', 'export', 'status', 'analyze', 'simulate'],
                       help='Command to execute')
    
    parser.add_argument('--simulate', action='store_true',
                       help='Use simulated NFC data (no hardware needed)')
    parser.add_argument('--from-file', type=str,
                       help='Read from binary EEPROM dump file')
    parser.add_argument('--csv', type=str, default='mykovolt_data.csv',
                       help='Output CSV file path')
    parser.add_argument('--days', type=float, default=7.0,
                       help='Days to simulate (default: 7)')
    parser.add_argument('--interval', type=float, default=15.0,
                       help='Measurement interval in minutes (default: 15)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show all entries')
    parser.add_argument('--json', action='store_true',
                       help='JSON output')
    parser.add_argument('--backend', choices=['simulate', 'libnfc', 'pcsc'],
                       default='simulate', help='NFC reader backend')
    
    args = parser.parse_args()
    
    if args.command == 'simulate':
        # Generate and save simulated data
        data = generate_simulated_data(days=args.days, interval_min=args.interval)
        tag = parse_tag_data(data)
        
        if args.json:
            print(json.dumps({
                'simulated': True,
                'days': args.days,
                'interval_min': args.interval,
                'total_entries': tag.total_entries,
                'first_ts': tag.first_ts,
                'last_ts': tag.last_ts,
                'avg_temp_c': tag.avg_temperature,
                'avg_cap_pf': tag.avg_capacitance,
                'v_batt_now': tag.v_batt_now,
            }, indent=2))
        else:
            format_tag_header(tag)
            format_entries(tag.entries, args.verbose)
            print(f"\n  💾 Saved to memory (simulated)")
        return
    
    # Connect to NFC reader or load from file
    if args.from_file:
        with open(args.from_file, 'rb') as f:
            eeprom_data = f.read()
        tag = parse_tag_data(eeprom_data)
    elif args.backend == 'simulate' or args.simulate:
        reader = NFCReader(backend='simulate')
        reader.connect()
        tags = reader.scan()
        if tags:
            eeprom_data = reader.read_eeprom(tags[0]['uid'])
            tag = parse_tag_data(eeprom_data)
        else:
            print("  No tags found.")
            return
        reader.close()
    else:
        reader = NFCReader(backend=args.backend)
        if not reader.connect():
            print("  ❌ Could not connect to NFC reader.")
            print("  Try --simulate for testing without hardware.")
            return
        tags = reader.scan()
        if tags:
            eeprom_data = reader.read_eeprom(tags[0]['uid'])
            tag = parse_tag_data(eeprom_data)
        else:
            print("  No MykoVolt tags found.")
            return
        reader.close()
    
    # Execute command
    if args.command == 'read' or args.command == 'scan':
        if args.json:
            output = {
                'device': 'MykoVolt DevKit',
                'firmware': tag.version,
                'interval_min': tag.interval_min,
                'v_batt_mv': tag.v_batt_now,
                'total_entries': tag.total_entries,
                'first_ts': tag.first_ts,
                'last_ts': tag.last_ts,
                'duration_hours': tag.duration_hours,
                'avg_temp_c': tag.avg_temperature,
                'avg_cap_pf': tag.avg_capacitance,
                'entries': [
                    {
                        'timestamp': e.timestamp,
                        'datetime': datetime.fromtimestamp(e.timestamp).strftime('%Y-%m-%d %H:%M:%S'),
                        'capacitance_pF': e.capacitance_pf,
                        'vwc_pct': round(vwc_from_capacitance(e.capacitance_pf), 1),
                        'temperature_C': e.temperature_c,
                        'v_batt_mV': e.v_batt_mv,
                        'flags': e.flags_human,
                    }
                    for e in tag.entries[-args.days:]
                ]
            }
            print(json.dumps(output, indent=2))
        else:
            format_tag_header(tag)
            format_entries(tag.entries, args.verbose)
    
    elif args.command == 'status':
        print(f"  Device:  MykoVolt DevKit v{tag.version}")
        print(f"  Entries: {tag.total_entries}/{MAX_ENTRIES} ({(tag.total_entries/MAX_ENTRIES)*100:.0f}% full)")
        print(f"  Period:  {tag.duration_hours:.1f} hours")
        print(f"  Battery: {tag.v_batt_now} mV {'✅' if tag.v_batt_now > 300 else '⚠️'}")
        print(f"  Avg Cap: {tag.avg_capacitance:.2f} pF" if tag.avg_capacitance else "")
        print(f"  Avg Temp: {tag.avg_temperature:.1f} °C" if tag.avg_temperature else "")
    
    elif args.command == 'export':
        output_csv(tag.entries, args.csv)
    
    elif args.command == 'analyze':
        analyze_moisture(tag.entries)


if __name__ == '__main__':
    main()
