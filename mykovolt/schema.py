"""FRAM ring buffer data model matching firmware format."""

from __future__ import annotations
import struct
from dataclasses import dataclass

FRAM_HEADER_SIZE = 256
FRAM_ENTRY_SIZE = 12
FRAM_ENTRY_SIZE_V2 = 13
FRAM_DATA_START = 0x100
FRAM_MAGIC = 0x4D56
FRAM_MAX_ENTRIES = 149
FRAM_MAX_ENTRIES_V2 = 137


def _xor_crc(data: bytes) -> int:
    crc = 0
    for b in data:
        crc ^= b
    return crc


def _parse_entries_impl(
    data: bytes, count: int, entry_size: int, entry_cls: type
) -> list:
    entries = []
    for i in range(count):
        offset = i * entry_size
        chunk = data[offset : offset + entry_size]
        if len(chunk) < entry_size:
            break
        entries.append(entry_cls.from_bytes(chunk))
    return entries


@dataclass
class RingBufferHeader:
    magic: int
    version: int
    write_ptr: int


@dataclass
class SensorEntry:
    timestamp: int
    capacitance_pf: float
    v_batt_mv: int
    v_sense_mv: int
    status: int
    crc_ok: bool

    @classmethod
    def from_bytes(cls, data: bytes) -> SensorEntry:
        if len(data) < FRAM_ENTRY_SIZE:
            raise ValueError(f"Need {FRAM_ENTRY_SIZE} bytes, got {len(data)}")
        ts, cap_x100, v_batt, v_sense, status = struct.unpack(">IHHHB", data[:11])
        stored_crc = data[11]
        computed_crc = _xor_crc(data[:11])
        return cls(
            timestamp=ts,
            capacitance_pf=cap_x100 / 100.0,
            v_batt_mv=v_batt,
            v_sense_mv=v_sense,
            status=status,
            crc_ok=(stored_crc == computed_crc),
        )


def parse_header(data: bytes) -> RingBufferHeader | None:
    if len(data) < 5:
        return None
    magic, version, write_ptr = struct.unpack(">HBH", data[:5])
    if magic != FRAM_MAGIC:
        return None
    return RingBufferHeader(magic=magic, version=version, write_ptr=write_ptr)


def parse_entries(data: bytes, count: int) -> list[SensorEntry]:
    return _parse_entries_impl(data, count, FRAM_ENTRY_SIZE, SensorEntry)


@dataclass
class TestFixtureEntry:
    __test__ = False

    timestamp: int
    voc_mv: int
    load_current_ma: int
    load_resistor_index: int
    temp_c: int
    humidity_pct: int
    status: int
    crc_ok: bool

    @classmethod
    def from_bytes(cls, data: bytes) -> TestFixtureEntry:
        if len(data) < FRAM_ENTRY_SIZE_V2:
            raise ValueError(f"Need {FRAM_ENTRY_SIZE_V2} bytes, got {len(data)}")
        ts, voc, load_ma, resistor, temp, rh, status = struct.unpack(
            ">IHhBbBB", data[:12]
        )
        stored_crc = data[12]
        computed_crc = _xor_crc(data[:12])
        return cls(
            timestamp=ts,
            voc_mv=voc,
            load_current_ma=load_ma,
            load_resistor_index=resistor,
            temp_c=temp,
            humidity_pct=rh,
            status=status,
            crc_ok=(stored_crc == computed_crc),
        )


def parse_entries_versioned(
    header: RingBufferHeader, data: bytes
) -> list[SensorEntry | TestFixtureEntry]:
    if header.write_ptr == 0:
        return []
    if header.version == 1:
        count = min(header.write_ptr // FRAM_ENTRY_SIZE, FRAM_MAX_ENTRIES)
        return parse_entries(data, count)
    elif header.version == 2:
        entry_size = FRAM_ENTRY_SIZE_V2
        count = min(header.write_ptr // entry_size, FRAM_MAX_ENTRIES_V2)
        return _parse_entries_impl(data, count, entry_size, TestFixtureEntry)
    else:
        raise ValueError(f"Unknown FRAM version {header.version}")
