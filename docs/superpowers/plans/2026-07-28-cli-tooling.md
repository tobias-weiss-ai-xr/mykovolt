# MykoVolt CLI Tooling Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a `mykovolt` Python package with Click CLI for fetching, parsing, calibrating, exporting, and plotting sensor data from the MykoVolt DevKit FRAM.

**Architecture:** Click-based CLI with ABC backend abstraction (I2C/NFC), dataclass schema matching firmware FRAM format, standalone subcommands plus combined `pipeline` command.

**Tech Stack:** Python 3.9+, Click 8.x, smbus2 (I2C), matplotlib (plot), pyarrow optional (Parquet)

---

### Task 1: Package Skeleton

**Files:**
- Create: `mykovolt/__init__.py`
- Create: `mykovolt/__main__.py`
- Create: `pyproject.toml`
- Test: `tests/test_cli.py`

- [ ] **Step 1: Write the package files**

```python
# mykovolt/__init__.py
"""MykoVolt — CLI tooling for the MykoVolt DevKit sensor platform."""
__version__ = "0.1.0"
```

```python
# mykovolt/__main__.py
"""Allow python -m mykovolt."""
from mykovolt.cli import cli

if __name__ == "__main__":
    cli()
```

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=64", "wheel"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "mykovolt"
version = "0.1.0"
description = "CLI tooling for MykoVolt DevKit sensor platform"
requires-python = ">=3.9"
dependencies = [
    "click>=8.0",
]

[project.scripts]
mykovolt = "mykovolt.cli:cli"

[tool.setuptools.packages.find]
include = ["mykovolt*"]
```

- [ ] **Step 2: Install package in dev mode**

```bash
pip install -e .
```

- [ ] **Step 3: Run basic smoke test**

```bash
python -c "import mykovolt; print(mykovolt.__version__)"
```
Expected: `0.1.0`

```bash
python -m mykovolt --help
```
Expected: top-level Click help (will show empty group for now)

- [ ] **Step 4: Commit**

```bash
git add mykovolt/ pyproject.toml
git commit -m "feat: scaffold mykovolt package with pyproject.toml"
```

---

### Task 2: Schema Dataclasses

**Files:**
- Create: `mykovolt/schema.py`
- Test: `tests/test_schema.py`

**Firmware FRAM format (from main.c):**
- Header at 0x000: magic(2B big-endian, 0x4D56 "MV") + version(1B) + write_ptr(2B big-endian, byte offset from 0x100) = 5 bytes meaningful, rest of 256B header unused
- Entries start at 0x100, 12 bytes each, max 149
- Entry: timestamp(4B big-endian) + cap_x100(2B big-endian) + v_batt_mv(2B big-endian) + v_sense_mv(2B big-endian) + status(1B) + crc(1B XOR of previous 11 bytes)

- [ ] **Step 1: Write the failing test**

```python
# tests/test_schema.py
import struct
from mykovolt.schema import RingBufferHeader, SensorEntry, parse_header, parse_entries

def test_parse_header_valid():
    data = struct.pack(">HBH", 0x4D56, 0x01, 0x0018)  # magic, version, write_ptr=24
    data += b"\x00" * 251  # pad to 256
    hdr = parse_header(data)
    assert hdr.magic == 0x4D56
    assert hdr.version == 0x01
    assert hdr.write_ptr == 24

def test_parse_header_invalid_magic():
    data = struct.pack(">HBH", 0x0000, 0x01, 0x0000)
    data += b"\x00" * 251
    hdr = parse_header(data)
    assert hdr is None

def test_parse_entry_valid():
    raw = struct.pack(">IHHHB", 1000, 12345, 3100, 1500, 0x03)
    crc = 0
    for b in raw:
        crc ^= b
    raw += bytes([crc])
    entry = SensorEntry.from_bytes(raw)
    assert entry.timestamp == 1000
    assert abs(entry.capacitance_pf - 123.45) < 0.01
    assert entry.v_batt_mv == 3100
    assert entry.v_sense_mv == 1500
    assert entry.status == 0x03
    assert entry.crc_ok is True

def test_parse_entry_bad_crc():
    raw = struct.pack(">IHHHB", 1000, 12345, 3100, 1500, 0x03)
    crc = 0
    for b in raw:
        crc ^= b
    raw += bytes([crc ^ 0xFF])  # corrupt CRC
    entry = SensorEntry.from_bytes(raw)
    assert entry.crc_ok is False

def test_parse_entries_empty():
    assert parse_entries(b"", 0) == []

def test_parse_entries_some():
    raw = b""
    for i in range(3):
        ts = 1000 + i * 60
        cap = 12000 + i * 100
        entry = struct.pack(">IHHHB", ts, cap, 3100, 1500, 0x01)
        crc = 0
        for b in entry:
            crc ^= b
        raw += entry + bytes([crc])
    entries = parse_entries(raw, 3)
    assert len(entries) == 3
    assert entries[0].timestamp == 1000
    assert entries[2].timestamp == 1120
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_schema.py -v
```
Expected: ModuleNotFoundError / ImportError

- [ ] **Step 3: Write implementation**

```python
# mykovolt/schema.py
"""FRAM ring buffer data model matching firmware format."""
from __future__ import annotations
import struct
from dataclasses import dataclass

FRAM_HEADER_SIZE = 256
FRAM_ENTRY_SIZE = 12
FRAM_DATA_START = 0x100
FRAM_MAGIC = 0x4D56
FRAM_MAX_ENTRIES = 149


@dataclass
class RingBufferHeader:
    magic: int
    version: int
    write_ptr: int  # byte offset from FRAM_DATA_START


@dataclass
class SensorEntry:
    timestamp: int       # seconds since RTC epoch
    capacitance_pf: float  # CIN1 in pF (from cap_x100 / 100)
    v_batt_mv: int
    v_sense_mv: int
    status: int          # bit0=VBAT_OK, bit1=RTC_ALARM
    crc_ok: bool         # True if CRC matches

    @classmethod
    def from_bytes(cls, data: bytes) -> SensorEntry:
        if len(data) < FRAM_ENTRY_SIZE:
            raise ValueError(f"Need {FRAM_ENTRY_SIZE} bytes, got {len(data)}")
        ts, cap_x100, v_batt, v_sense, status = struct.unpack(">IHHHB", data[:11])
        stored_crc = data[11]
        computed_crc = 0
        for b in data[:11]:
            computed_crc ^= b
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
    entries = []
    for i in range(count):
        offset = i * FRAM_ENTRY_SIZE
        chunk = data[offset:offset + FRAM_ENTRY_SIZE]
        if len(chunk) < FRAM_ENTRY_SIZE:
            break
        entries.append(SensorEntry.from_bytes(chunk))
    return entries
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/test_schema.py -v
```
Expected: All 6 tests pass

- [ ] **Step 5: Commit**

```bash
git add mykovolt/schema.py tests/test_schema.py
git commit -m "feat: add FRAM schema dataclasses with parse_header and parse_entries"
```

---

### Task 3: Backends (ABC + I2C + NFC)

**Files:**
- Create: `mykovolt/backend.py`
- Test: `tests/test_backend.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_backend.py
import pytest
from mykovolt.backend import Backend, I2cBackend, NfcBackend

def test_backend_abc_cannot_instantiate():
    with pytest.raises(TypeError):
        Backend()

def test_i2c_backend_read_raises_without_smbus():
    """Without smbus2 installed, I2cBackend read should give clear error."""
    backend = I2cBackend(bus=1, addr=0x50)
    with pytest.raises(RuntimeError, match="smbus2"):
        backend.read(0x00, 10)

def test_nfc_backend_not_implemented():
    backend = NfcBackend()
    with pytest.raises(NotImplementedError):
        backend.read(0x00, 10)

def test_i2c_backend_properties():
    backend = I2cBackend(bus=0, addr=0x51)
    assert backend.bus == 0
    assert backend.addr == 0x51
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_backend.py -v
```
Expected: ModuleNotFoundError

- [ ] **Step 3: Write implementation**

```python
# mykovolt/backend.py
"""Device communication backends for reading FRAM data."""
from __future__ import annotations
from abc import ABC, abstractmethod


class Backend(ABC):
    @abstractmethod
    def read(self, addr: int, length: int) -> bytes:
        ...


class I2cBackend(Backend):
    def __init__(self, bus: int = 1, addr: int = 0x50):
        self.bus = bus
        self.addr = addr
        self._dev = None

    def read(self, addr: int, length: int) -> bytes:
        if self._dev is None:
            try:
                import smbus2
                self._dev = smbus2.SMBus(self.bus)
            except ImportError:
                raise RuntimeError(
                    "smbus2 not installed. Run: pip install smbus2"
                )
        # MB85RC16 uses 16-bit register addressing
        reg_hi = (addr >> 8) & 0xFF
        reg_lo = addr & 0xFF
        self._dev.write_i2c_block_data(self.addr, reg_hi, [reg_lo])
        return bytes(self._dev.read_i2c_block_data(self.addr, reg_hi, length))


class NfcBackend(Backend):
    def __init__(self):
        self._tag = None

    def read(self, addr: int, length: int) -> bytes:
        raise NotImplementedError("NFC backend requires an NFC reader")
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/test_backend.py -v
```
Expected: All 4 tests pass

- [ ] **Step 5: Commit**

```bash
git add mykovolt/backend.py tests/test_backend.py
git commit -m "feat: add Backend ABC, I2cBackend with smbus2, NfcBackend stub"
```

---

### Task 4: FRAM Reader

**Files:**
- Create: `mykovolt/fram.py`
- Test: `tests/test_fram.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_fram.py
import struct
import pytest
from mykovolt.schema import RingBufferHeader, SensorEntry
from mykovolt.backend import Backend
from mykovolt.fram import read_fram

class MockBackend(Backend):
    def __init__(self, fram_data: bytes):
        self.fram_data = fram_data

    def read(self, addr: int, length: int) -> bytes:
        if addr + length > len(self.fram_data):
            return self.fram_data[addr:]
        return self.fram_data[addr:addr + length]

def make_fram(entries: list[bytes]) -> bytes:
    header = struct.pack(">HBH", 0x4D56, 0x01, len(entries) * 12)
    header = header.ljust(256, b"\x00")
    data = bytearray(header)
    for entry in entries:
        crc = 0
        for b in entry:
            crc ^= b
        data.extend(entry + bytes([crc]))
    return bytes(data)

def test_read_fram_empty():
    data = make_fram([])
    backend = MockBackend(data)
    header, entries = read_fram(backend)
    assert header.magic == 0x4D56
    assert len(entries) == 0

def test_read_fram_three_entries():
    raw_entries = []
    for i in range(3):
        ts = 1000 + i * 60
        raw_entries.append(struct.pack(">IHHHB", ts, 12345, 3100, 1500, 0x01))
    data = make_fram(raw_entries)
    backend = MockBackend(data)
    header, entries = read_fram(backend)
    assert len(entries) == 3

def test_read_fram_corrupt_header():
    data = b"\x00" * 2048
    backend = MockBackend(data)
    with pytest.raises(ValueError, match="magic"):
        read_fram(backend)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_fram.py -v
```
Expected: ModuleNotFoundError

- [ ] **Step 3: Write implementation**

```python
# mykovolt/fram.py
"""Read FRAM ring buffer via a Backend."""
from mykovolt.schema import (
    RingBufferHeader,
    SensorEntry,
    parse_header,
    parse_entries,
    FRAM_HEADER_SIZE,
    FRAM_DATA_START,
    FRAM_MAX_ENTRIES,
)
from mykovolt.backend import Backend

FRAM_TOTAL_SIZE = 2048  # MB85RC16 is 16Kbit


def read_fram(backend: Backend) -> tuple[RingBufferHeader, list[SensorEntry]]:
    header_raw = backend.read(0x00, FRAM_HEADER_SIZE)
    header = parse_header(header_raw)
    if header is None:
        raise ValueError("Invalid FRAM magic — device not initialized or wrong backend")
    if header.write_ptr == 0:
        return header, []
    entry_count = min(header.write_ptr // 12, FRAM_MAX_ENTRIES)
    entries_raw = backend.read(FRAM_DATA_START, entry_count * 12)
    entries = parse_entries(entries_raw, entry_count)
    return header, entries
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/test_fram.py -v
```
Expected: All 3 tests pass

- [ ] **Step 5: Commit**

```bash
git add mykovolt/fram.py tests/test_fram.py
git commit -m "feat: add FRAM reader with backend abstraction"
```

---

### Task 5: Calibration

**Files:**
- Create: `mykovolt/calibrate.py`
- Test: `tests/test_calibrate.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_calibrate.py
import json
import pytest
from mykovolt.schema import SensorEntry
from mykovolt.calibrate import Calibration, load_calibration, apply_calibration

def test_load_calibration(tmp_path):
    cal_file = tmp_path / "cal.json"
    cal_file.write_text(json.dumps([
        {"channel": "CIN1", "offset_pf": 0.5, "gain": 1.02},
    ]))
    cal = load_calibration(str(cal_file))
    assert cal.offsets.get("CIN1", 0.0) == 0.5
    assert cal.gains.get("CIN1", 1.0) == 1.02

def test_calibration_file_not_found():
    cal = load_calibration("/nonexistent/cal.json")
    assert len(cal.offsets) == 0  # returns empty calibration

def test_apply_calibration_default():
    entry = SensorEntry(1000, 123.45, 3100, 1500, 0x01, True)
    cal = Calibration()  # empty, no calibration
    result = apply_calibration(entry, cal)
    assert abs(result.capacitance_pf - 123.45) < 0.01

def test_apply_calibration_with_offset_gain():
    entry = SensorEntry(1000, 123.45, 3100, 1500, 0x01, True)
    cal = Calibration(offsets={"CIN1": -0.5}, gains={"CIN1": 1.05})
    result = apply_calibration(entry, cal)
    expected = (123.45 + 0.5) * 1.05  # offset is subtracted from raw
    assert abs(result.capacitance_pf - expected) < 0.01
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_calibrate.py -v
```
Expected: ModuleNotFoundError

- [ ] **Step 3: Write implementation**

```python
# mykovolt/calibrate.py
"""Offset/gain calibration for sensor channels."""
from __future__ import annotations
import json
from dataclasses import dataclass, field
from mykovolt.schema import SensorEntry


@dataclass
class Calibration:
    offsets: dict[str, float] = field(default_factory=dict)
    gains: dict[str, float] = field(default_factory=dict)


def load_calibration(path: str) -> Calibration:
    try:
        with open(path) as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return Calibration()
    offsets = {}
    gains = {}
    for item in data:
        ch = item.get("channel", "CIN1")
        offsets[ch] = item.get("offset_pf", 0.0)
        gains[ch] = item.get("gain", 1.0)
    return Calibration(offsets=offsets, gains=gains)


def apply_calibration(entry: SensorEntry, cal: Calibration) -> SensorEntry:
    raw_pf = entry.capacitance_pf
    offset = cal.offsets.get("CIN1", 0.0)
    gain = cal.gains.get("CIN1", 1.0)
    calibrated = (raw_pf + offset) * gain
    return SensorEntry(
        timestamp=entry.timestamp,
        capacitance_pf=calibrated,
        v_batt_mv=entry.v_batt_mv,
        v_sense_mv=entry.v_sense_mv,
        status=entry.status,
        crc_ok=entry.crc_ok,
    )
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/test_calibrate.py -v
```
Expected: All 4 tests pass

- [ ] **Step 5: Commit**

```bash
git add mykovolt/calibrate.py tests/test_calibrate.py
git commit -m "feat: add calibration loading and offset/gain application"
```

---

### Task 6: Export (CSV / JSON / Parquet)

**Files:**
- Create: `mykovolt/export.py`
- Test: `tests/test_export.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_export.py
import json
import csv
import io
import pytest
from mykovolt.schema import SensorEntry
from mykovolt.export import export_csv, export_json, export_parquet

def make_entries():
    return [
        SensorEntry(1000, 123.45, 3100, 1500, 0x01, True),
        SensorEntry(1060, 124.10, 3080, 1490, 0x03, True),
    ]

def test_export_csv():
    entries = make_entries()
    buf = io.StringIO()
    export_csv(entries, buf)
    buf.seek(0)
    reader = csv.DictReader(buf)
    rows = list(reader)
    assert len(rows) == 2
    assert rows[0]["timestamp"] == "1000"
    assert rows[0]["capacitance_pf"] == "123.45"

def test_export_json():
    entries = make_entries()
    buf = io.StringIO()
    export_json(entries, buf)
    buf.seek(0)
    data = json.load(buf)
    assert len(data) == 2
    assert data[0]["timestamp"] == 1000

def test_export_json_empty():
    buf = io.StringIO()
    export_json([], buf)
    buf.seek(0)
    assert json.load(buf) == []

def test_export_parquet_not_installed():
    entries = make_entries()
    with pytest.raises(RuntimeError, match="pyarrow"):
        export_parquet(entries, "data.parquet")
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_export.py -v
```
Expected: ModuleNotFoundError

- [ ] **Step 3: Write implementation**

```python
# mykovolt/export.py
"""Export sensor entries to CSV, JSON, or Parquet."""
from __future__ import annotations
import csv
import json
import io
from typing import TextIO
from mykovolt.schema import SensorEntry


def _row(entry: SensorEntry) -> dict:
    return {
        "timestamp": entry.timestamp,
        "capacitance_pf": entry.capacitance_pf,
        "v_batt_mv": entry.v_batt_mv,
        "v_sense_mv": entry.v_sense_mv,
        "status": entry.status,
        "crc_ok": entry.crc_ok,
    }


def export_csv(entries: list[SensorEntry], buf: TextIO) -> None:
    if not entries:
        return
    writer = csv.DictWriter(buf, fieldnames=list(_row(entries[0]).keys()))
    writer.writeheader()
    for entry in entries:
        writer.writerow(_row(entry))


def export_json(entries: list[SensorEntry], buf: TextIO) -> None:
    json.dump([_row(e) for e in entries], buf, indent=2)


def export_parquet(entries: list[SensorEntry], path: str) -> None:
    try:
        import pandas as pd
        import pyarrow  # noqa: F401
    except ImportError:
        raise RuntimeError(
            "Parquet export requires pandas and pyarrow. "
            "Run: pip install pandas pyarrow"
        )
    df = pd.DataFrame([_row(e) for e in entries])
    df.to_parquet(path, index=False)
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/test_export.py -v
```
Expected: All 4 tests pass

- [ ] **Step 5: Commit**

```bash
git add mykovolt/export.py tests/test_export.py
git commit -m "feat: add CSV/JSON/Parquet export for sensor entries"
```

---

### Task 7: Quick-Look Plot

**Files:**
- Create: `mykovolt/plot.py`
- Test: `tests/test_plot.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_plot.py
import pytest
from mykovolt.schema import SensorEntry
from mykovolt.plot import plot_timeseries, plot_summary

def make_entries():
    return [
        SensorEntry(1000, 123.45, 3100, 1500, 0x01, True),
        SensorEntry(1060, 124.10, 3080, 1490, 0x03, True),
        SensorEntry(1120, 122.80, 3050, 1480, 0x01, True),
        SensorEntry(1180, 125.30, 3020, 1470, 0x03, True),
    ]

def test_plot_timeseries_creates_figure():
    fig = plot_timeseries(make_entries())
    assert fig is not None
    import matplotlib
    assert isinstance(fig, matplotlib.figure.Figure)

def test_plot_summary_creates_figure():
    fig = plot_summary(make_entries())
    assert fig is not None
    import matplotlib
    assert isinstance(fig, matplotlib.figure.Figure)

def test_plot_empty_returns_none():
    assert plot_timeseries([]) is None
    assert plot_summary([]) is None
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_plot.py -v
```
Expected: ModuleNotFoundError

- [ ] **Step 3: Write implementation**

```python
# mykovolt/plot.py
"""Quick-look matplotlib plots for sensor data."""
from __future__ import annotations
from mykovolt.schema import SensorEntry


def plot_timeseries(entries: list[SensorEntry]):
    if not entries:
        return None
    import matplotlib.pyplot as plt
    times = [e.timestamp for e in entries]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    ax1.plot(times, [e.capacitance_pf for e in entries], "b.-")
    ax1.set_ylabel("Capacitance (pF)")
    ax1.grid(True)
    ax2.plot(times, [e.v_batt_mv for e in entries], "r.-", label="V_batt")
    ax2.plot(times, [e.v_sense_mv for e in entries], "g.-", label="V_sense")
    ax2.set_xlabel("Timestamp (s)")
    ax2.set_ylabel("Voltage (mV)")
    ax2.legend()
    ax2.grid(True)
    fig.tight_layout()
    return fig


def plot_summary(entries: list[SensorEntry]):
    if not entries:
        return None
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(10, 6))
    caps = [e.capacitance_pf for e in entries]
    axes[0, 0].hist(caps, bins=10, edgecolor="black")
    axes[0, 0].set_xlabel("Capacitance (pF)")
    axes[0, 0].set_ylabel("Count")
    axes[0, 0].set_title("Capacitance Distribution")
    axes[0, 1].plot([e.v_batt_mv for e in entries], [e.v_sense_mv for e in entries], ".")
    axes[0, 1].set_xlabel("V_batt (mV)")
    axes[0, 1].set_ylabel("V_sense (mV)")
    axes[0, 1].set_title("Voltage Correlation")
    crc_ok = sum(1 for e in entries if e.crc_ok)
    crc_bad = len(entries) - crc_ok
    axes[1, 0].bar(["CRC OK", "CRC Bad"], [crc_ok, crc_bad])
    axes[1, 0].set_title("Data Integrity")
    vt = [e.status & 1 for e in entries]
    rt = [(e.status >> 1) & 1 for e in entries]
    axes[1, 1].plot(times := list(range(len(entries))), vt, "g|", label="VBAT_OK")
    axes[1, 1].plot(times, rt, "r|", label="RTC_ALARM")
    axes[1, 1].set_xlabel("Entry #")
    axes[1, 1].set_title("Status Flags")
    axes[1, 1].legend()
    fig.tight_layout()
    return fig
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/test_plot.py -v
```
Expected: All 3 tests pass

- [ ] **Step 5: Commit**

```bash
git add mykovolt/plot.py tests/test_plot.py
git commit -m "feat: add quick-look matplotlib plots (timeseries + summary)"
```

---

### Task 8: CLI with Pipeline

**Files:**
- Create: `mykovolt/cli.py`
- Create: `mykovolt/pipeline.py`
- Modify: `tests/test_cli.py` (extend with Click runner tests)

- [ ] **Step 1: Write the failing test**

```python
# tests/test_cli.py (extend existing file)
from click.testing import CliRunner
from mykovolt.cli import cli

runner = CliRunner()

def test_cli_help():
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "pipeline" in result.output
    assert "fetch" in result.output
    assert "parse" in result.output
    assert "calibrate" in result.output
    assert "export" in result.output
    assert "plot" in result.output

def test_cli_fetch_no_backend():
    result = runner.invoke(cli, ["fetch"])
    assert result.exit_code != 0

def test_cli_parse_help():
    result = runner.invoke(cli, ["parse", "--help"])
    assert result.exit_code == 0
    assert "INPUT" in result.output

def test_cli_parse_valid_file(tmp_path):
    import struct
    data = struct.pack(">HBH", 0x4D56, 0x01, 12)
    data = data.ljust(256, b"\x00")
    entry = struct.pack(">IHHHB", 1000, 12345, 3100, 1500, 0x01)
    crc = 0
    for b in entry:
        crc ^= b
    data += entry + bytes([crc])
    fram_file = tmp_path / "fram.bin"
    fram_file.write_bytes(data)
    result = runner.invoke(cli, ["parse", str(fram_file)])
    assert result.exit_code == 0
    assert "1000" in result.output
    assert "123.45" in result.output

def test_cli_pipeline_help():
    result = runner.invoke(cli, ["pipeline", "--help"])
    assert result.exit_code == 0
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_cli.py -v
```
Expected: Test failures (cli module not found yet)

- [ ] **Step 3: Write pipeline module**

```python
# mykovolt/pipeline.py
"""Combined fetch→parse→calibrate→export pipeline."""
from __future__ import annotations
from mykovolt.backend import Backend
from mykovolt.fram import read_fram
from mykovolt.calibrate import load_calibration, apply_calibration
from mykovolt.export import export_csv, export_json
from mykovolt.schema import SensorEntry


def run_pipeline(
    backend: Backend,
    cal_path: str | None = None,
    fmt: str = "csv",
) -> list[SensorEntry]:
    header, entries = read_fram(backend)
    if cal_path:
        cal = load_calibration(cal_path)
        entries = [apply_calibration(e, cal) for e in entries]
    return entries
```

- [ ] **Step 4: Write CLI module**

```python
# mykovolt/cli.py
"""Click-based CLI for MykoVolt DevKit."""
from __future__ import annotations
import sys
import click
from mykovolt import __version__
from mykovolt.backend import I2cBackend
from mykovolt.fram import read_fram
from mykovolt.calibrate import load_calibration, apply_calibration
from mykovolt.export import export_csv, export_json
from mykovolt.plot import plot_timeseries, plot_summary
from mykovolt.pipeline import run_pipeline


@click.group()
@click.version_option(version=__version__)
def cli():
    """MykoVolt DevKit — sensor data tooling."""


@cli.command()
@click.option("--backend", type=click.Choice(["i2c", "nfc"]), default="i2c")
@click.option("--bus", default=1, help="I2C bus number")
@click.option("--addr", default=0x50, help="FRAM I2C address", type=int)
@click.option("--output", "-o", default=None, help="Output file")
@click.option("--format", "-f", "fmt", default="csv", help="Output format")
@click.option("--calibration", "-c", default=None, help="Calibration JSON file")
def pipeline(backend, bus, addr, output, fmt, calibration):
    """Fetch, parse, calibrate, and export in one command."""
    if backend == "i2c":
        dev = I2cBackend(bus=bus, addr=addr)
    else:
        click.echo("NFC backend not yet implemented", err=True)
        sys.exit(1)
    try:
        entries = run_pipeline(dev, cal_path=calibration, fmt=fmt)
    except (ValueError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    if not entries:
        click.echo("No entries found", err=True)
        sys.exit(0)
    buf = open(output, "w") if output else sys.stdout
    if fmt == "csv":
        export_csv(entries, buf)
    else:
        export_json(entries, buf)
    if output:
        buf.close()
        click.echo(f"Wrote {len(entries)} entries to {output}")


@cli.command()
@click.option("--backend", type=click.Choice(["i2c", "nfc"]), default="i2c")
@click.option("--bus", default=1, help="I2C bus number")
@click.option("--addr", default=0x50, help="FRAM I2C address", type=int)
def fetch(backend, bus, addr):
    """Read raw FRAM data from device."""
    if backend == "i2c":
        dev = I2cBackend(bus=bus, addr=addr)
    else:
        click.echo("NFC backend not yet implemented", err=True)
        sys.exit(1)
    try:
        header, entries = read_fram(dev)
    except (ValueError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    click.echo(f"Header: magic=0x{header.magic:04X} version={header.version} "
               f"write_ptr={header.write_ptr}")
    click.echo(f"Entries: {len(entries)}")
    for e in entries:
        click.echo(f"  ts={e.timestamp} cap={e.capacitance_pf:.2f}pF "
                   f"Vbatt={e.v_batt_mv}mV Vsense={e.v_sense_mv}mV "
                   f"status=0x{e.status:02x} crc={'OK' if e.crc_ok else 'BAD'}")


@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.option("--output", "-o", default=None, help="Output file")
@click.option("--format", "-f", "fmt", default="csv", help="Output format")
@click.option("--calibration", "-c", default=None, help="Calibration JSON file")
def parse(input, output, fmt, calibration):
    """Parse raw FRAM binary dump."""
    with open(input, "rb") as f:
        data = f.read()
    from mykovolt.schema import parse_header, parse_entries, FRAM_DATA_START, FRAM_MAX_ENTRIES
    header = parse_header(data)
    if header is None:
        click.echo("Invalid FRAM header", err=True)
        sys.exit(1)
    count = min(header.write_ptr // 12, FRAM_MAX_ENTRIES)
    offset = FRAM_DATA_START
    entries = parse_entries(data[offset:], count)
    if calibration:
        cal = load_calibration(calibration)
        entries = [apply_calibration(e, cal) for e in entries]
    click.echo(f"Parsed {len(entries)} entries")
    buf = open(output, "w") if output else sys.stdout
    if fmt == "csv":
        export_csv(entries, buf)
    else:
        export_json(entries, buf)
    if output:
        buf.close()


@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.option("--output", "-o", default="calibration.json", help="Output file")
def calibrate(input, output):
    """Generate calibration from known reference data."""
    click.echo("Calibration generation not yet implemented", err=True)


@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.option("--output", "-o", default="plot.png", help="Output image")
@click.option("--type", "plot_type", default="timeseries",
              type=click.Choice(["timeseries", "summary"]))
def plot(input, output, plot_type):
    """Plot sensor data from a CSV/JSON export."""
    import json, csv
    from mykovolt.schema import SensorEntry
    if input.endswith(".json"):
        with open(input) as f:
            rows = json.load(f)
    else:
        with open(input, newline="") as f:
            rows = list(csv.DictReader(f))
    entries = [
        SensorEntry(
            timestamp=int(r["timestamp"]),
            capacitance_pf=float(r["capacitance_pf"]),
            v_batt_mv=int(r["v_batt_mv"]),
            v_sense_mv=int(r["v_sense_mv"]),
            status=int(r["status"]),
            crc_ok=r.get("crc_ok", "True") == "True",
        )
        for r in rows
    ]
    fn = plot_timeseries if plot_type == "timeseries" else plot_summary
    fig = fn(entries)
    if fig is None:
        click.echo("No data to plot", err=True)
        sys.exit(1)
    fig.savefig(output, dpi=150)
    click.echo(f"Plot saved to {output}")
```

- [ ] **Step 5: Run test to verify it passes**

```bash
pytest tests/test_cli.py -v
```
Expected: All 5 tests pass

- [ ] **Step 6: Commit**

```bash
git add mykovolt/cli.py mykovolt/pipeline.py tests/test_cli.py
git commit -m "feat: add CLI (pipeline/fetch/parse/calibrate/plot) with pipeline orchestration"
```