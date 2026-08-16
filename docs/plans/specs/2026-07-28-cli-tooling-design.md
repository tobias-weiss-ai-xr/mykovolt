# MykoVolt CLI Tooling — `mykovolt` Python Package

## Problem

Sensor data lives on the device FRAM (149 entries × 12 bytes) and can be fetched via I2C (while running) or NFC (after deployment). Today there is no tooling to read, parse, calibrate, export, or plot this data. Six standalone argparse scripts exist in `tools/` but no unified CLI.

## Architecture

A `mykovolt/` Python package with a Click-based CLI, a protocol layer for device communication, and a data model for sensor records.

```
                    ┌──────────────────┐
                    │   mykovolt CLI   │
                    │  (click group)   │
                    └──┬──┬──┬──┬──┬──┘
                       │  │  │  │  │
              ┌────────┘  │  │  │  └──────────┐
              │    ┌──────┘  │  └──────┐       │
              ▼    ▼         ▼         ▼       ▼
         ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
         │fetch │ │parse │ │cal   │ │export│ │plot  │
         └──┬───┘ └──────┘ └──────┘ └──────┘ └──────┘
            │         ▲         ▲
            ▼         │         │
         ┌────────────┴─────────┴──────────┐
         │        Backends (ABC)            │
         │  I2cBackend   NfcBackend         │
         └──────────────────────────────────┘
```

`pipeline` combines fetch→parse→calibrate→export in one command.

## Package Structure

```
mykovolt/
├── __init__.py          # version
├── __main__.py          # python -m mykovolt
├── cli.py               # click group + subcommands
├── backend.py           # Backend ABC + I2cBackend + NfcBackend
├── schema.py            # RingBufferHeader, SensorEntry dataclasses
├── fram.py              # FRAM read (header + entries)
├── pipeline.py          # full pipeline logic
├── calibrate.py         # offset/gain calibration
├── export.py            # CSV / JSON / Parquet export
└── plot.py              # matplotlib quick-look plots
```

## Data Model

```python
@dataclass
class RingBufferHeader:
    magic: int           # 0xA5A5
    version: int         # 1
    write_ptr: int       # 0-148

@dataclass
class SensorEntry:
    timestamp: int       # seconds since RTC epoch
    capacitance_pf: float # CIN1 in pF
    v_batt_mv: int       # battery voltage
    v_sense_mv: int      # sensor excitation voltage
    status: int          # bitfield: bit0=VBAT_OK, bit1=RTC_ALARM
    crc: int             # CRC16 of previous fields
```

## Subcommands

| Command | Description |
|---------|-------------|
| `mykovolt pipeline` | fetch → parse → calibrate → export (one-shot) |
| `mykovolt fetch` | Read FRAM ring buffer via selected backend |
| `mykovolt parse` | Convert raw bytes to SensorEntry list |
| `mykovolt calibrate` | Apply offset/gain from calibration file |
| `mykovolt export` | Write to CSV / JSON / Parquet |
| `mykovolt plot` | Quick-look plot of capacitance / voltage vs time |

## Backends

```python
class Backend(ABC):
    @abstractmethod
    def read(self, addr: int, length: int) -> bytes: ...

class I2cBackend(Backend):
    # smbus2 / python-periphery I2C, 0x50, 16-bit register addr
    def read(self, addr, length): ...

class NfcBackend(Backend):
    # st25dv04k mailbox read via ndef / pynfc
    def read(self, addr, length): ...
```

## Errors

- Backend connection failure → `click.ClickException("no device found")`
- Ring buffer header invalid (magic mismatch) → `click.ClickException("invalid FRAM header")`
- CRC mismatch on entry → warn + skip, continue pipeline
- Calibration file missing → fall back to raw values with warning

## Files

- `mykovolt/` — new package at repo root
- `pyproject.toml` — at repo root (adds to existing)
- Tests in `tests/test_cli.py`

## Testing

- Unit tests for schema, fram parsing, calibration (no hardware)
- Click runner for CLI invocation
- Integration test with fixture files (pre-recorded FRAM dump)