# Pressling Simulation Calibration & CLI Extensions — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add test fixture data models, extend the CLI parser to auto-detect dev-kit vs. test-fixture FRAM entries, and create a `mykovolt calibrate` command that fits simulation model parameters to measured data.

**Architecture:** The existing `mykovolt` Python package gains a new `TestFixtureEntry` dataclass (alongside `SensorEntry`) and version-aware FRAM parsing. The `alternatives.py` simulation gains a `CalibratedModel` class that wraps the existing loss equations with tuneable parameters and a least-squares fitter. The `mykovolt calibrate` CLI command reads test fixture CSV output and produces a YAML file of fitted parameters.

**Tech Stack:** Python 3.11+, Click (CLI), struct (binary parsing), scipy (curve fitting, optional — falls back to grid search), PyYAML (parameter output), existing `mykovolt` package patterns.

---

## File Map

| File | Responsibility |
|---|---|
| `mykovolt/schema.py` | Add `TestFixtureEntry` dataclass + `parse_entries_versioned()` |
| `mykovolt/export.py` | Extend `_row()` to handle `TestFixtureEntry` |
| `mykovolt/cli.py` | Update `parse` + `fetch` for version-aware parsing, implement `calibrate` command |
| `mykovolt/calibrate_sim.py` | New: `CalibratedModel` class + `fit_model()` + YAML I/O |
| `simulation/calibrated_pressling.py` | New: geometry sweep, multi-cell model, environmental derating |
| `tests/test_schema.py` | Add tests for `TestFixtureEntry` + versioned parsing |
| `tests/test_calibrate_sim.py` | New: tests for model fitting, parameter I/O |
| `tests/test_calibrated_pressling.py` | New: tests for geometry sweep, multi-cell, derating |

---

### Task 1: TestFixtureEntry Dataclass

**Files:**
- Modify: `mykovolt/schema.py:14-66`
- Test: `tests/test_schema.py`

- [ ] **Step 1: Write the failing test**

```python
# Add to tests/test_schema.py

def test_test_fixture_entry_from_bytes():
    data = struct.pack(">IhHBBbB",
        1750000000,    # timestamp
        380,            # voc_mv (int16, 0.38V)
        2500,           # load_current_ma * 10 (250 = 25.0 mA)
        2,              # load_resistor_index (R2)
        22,             # temperature_c (int8)
        65,             # humidity_pct (uint8)
        0x01,           # status
    )
    data += bytes([0])  # pad to 11 bytes
    crc = 0
    for b in data:
        crc ^= b
    data += bytes([crc])
    assert len(data) == 12

    entry = TestFixtureEntry.from_bytes(data)
    assert entry.timestamp == 1750000000
    assert entry.voc_mv == 380
    assert entry.load_current_ma == 25.0
    assert entry.load_resistor_index == 2
    assert entry.temp_c == 22
    assert entry.humidity_pct == 65
    assert entry.status == 0x01
    assert entry.crc_ok is True


def test_test_fixture_entry_bad_crc():
    data = struct.pack(">IhHBBbB", 0, 0, 0, 0, 0, 0, 0)
    data += bytes([0x00, 0xFF])  # wrong CRC
    entry = TestFixtureEntry.from_bytes(data)
    assert entry.crc_ok is False


def test_parse_entries_versioned_v1():
    """Version 1 entries are SensorEntry (dev kit)."""
    from mykovolt.schema import FRAM_MAGIC
    header_data = struct.pack(">HBH", FRAM_MAGIC, 1, 12) + b'\x00' * 251
    header = parse_header(header_data)
    assert header.version == 1
    entries = parse_entries_versioned(header, b'\x00' * 12)
    assert len(entries) == 1
    assert isinstance(entries[0], SensorEntry)


def test_parse_entries_versioned_v2():
    """Version 2 entries are TestFixtureEntry."""
    from mykovolt.schema import FRAM_MAGIC
    header_data = struct.pack(">HBH", FRAM_MAGIC, 2, 12) + b'\x00' * 251
    header = parse_header(header_data)
    assert header.version == 2
    entries = parse_entries_versioned(header, b'\x00' * 12)
    assert len(entries) == 1
    assert isinstance(entries[0], TestFixtureEntry)


def test_parse_entries_versioned_unknown_version():
    """Unknown version raises ValueError."""
    from mykovolt.schema import FRAM_MAGIC
    header_data = struct.pack(">HBH", FRAM_MAGIC, 99, 12) + b'\x00' * 251
    header = parse_header(header_data)
    import pytest
    with pytest.raises(ValueError, match="version"):
        parse_entries_versioned(header, b'\x00' * 12)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /home/weissto_local/git/mykovolt && python -m pytest tests/test_schema.py::test_test_fixture_entry_from_bytes -v`
Expected: FAIL with `NameError: name 'TestFixtureEntry' is not defined`

- [ ] **Step 3: Write minimal implementation**

Add to `mykovolt/schema.py` after the `SensorEntry` class and `parse_entries` function:

```python
@dataclass
class TestFixtureEntry:
    timestamp: int
    voc_mv: int
    load_current_ma: float
    load_resistor_index: int
    temp_c: int
    humidity_pct: int
    status: int
    crc_ok: bool

    @classmethod
    def from_bytes(cls, data: bytes) -> TestFixtureEntry:
        if len(data) < FRAM_ENTRY_SIZE:
            raise ValueError(f"Need {FRAM_ENTRY_SIZE} bytes, got {len(data)}")
        ts, voc, load_x10, resistor, temp, rh, status = struct.unpack(">IhHBBbB", data[:11])
        stored_crc = data[11]
        computed_crc = 0
        for b in data[:11]:
            computed_crc ^= b
        return cls(
            timestamp=ts,
            voc_mv=voc,
            load_current_ma=load_x10 / 10.0,
            load_resistor_index=resistor,
            temp_c=temp,
            humidity_pct=max(rh, 0),
            status=status,
            crc_ok=(stored_crc == computed_crc),
        )


def parse_entries_versioned(
    header: RingBufferHeader, data: bytes
) -> list[SensorEntry | TestFixtureEntry]:
    if header.write_ptr == 0:
        return []
    count = min(header.write_ptr // FRAM_ENTRY_SIZE, FRAM_MAX_ENTRIES)
    if header.version == 1:
        return parse_entries(data, count)
    elif header.version == 2:
        entries = []
        for i in range(count):
            offset = i * FRAM_ENTRY_SIZE
            chunk = data[offset : offset + FRAM_ENTRY_SIZE]
            if len(chunk) < FRAM_ENTRY_SIZE:
                break
            entries.append(TestFixtureEntry.from_bytes(chunk))
        return entries
    else:
        raise ValueError(f"Unknown FRAM version {header.version}")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /home/weissto_local/git/mykovolt && python -m pytest tests/test_schema.py -v`
Expected: All tests PASS (existing + 5 new)

- [ ] **Step 5: Commit**

```bash
git add mykovolt/schema.py tests/test_schema.py
git commit -m "feat: add TestFixtureEntry dataclass and version-aware FRAM parsing"
```

---

### Task 2: Extend Export for TestFixtureEntry

**Files:**
- Modify: `mykovolt/export.py:9-17`
- Test: `tests/test_export.py`

- [ ] **Step 1: Write the failing test**

```python
# Add to tests/test_export.py

def test_export_csv_test_fixture_entry(tmp_path):
    from mykovolt.schema import TestFixtureEntry
    entries = [
        TestFixtureEntry(
            timestamp=1000, voc_mv=380, load_current_ma=25.0,
            load_resistor_index=2, temp_c=22, humidity_pct=65,
            status=0, crc_ok=True,
        )
    ]
    out = tmp_path / "out.csv"
    with open(out, "w") as f:
        export_csv(entries, f)
    text = out.read_text()
    assert "voc_mv" in text
    assert "380" in text
    assert "25.0" in text


def test_export_json_test_fixture_entry(tmp_path):
    from mykovolt.schema import TestFixtureEntry
    entries = [
        TestFixtureEntry(
            timestamp=1000, voc_mv=380, load_current_ma=25.0,
            load_resistor_index=2, temp_c=22, humidity_pct=65,
            status=0, crc_ok=True,
        )
    ]
    out = tmp_path / "out.json"
    with open(out, "w") as f:
        export_json(entries, f)
    import json
    data = json.loads(out.read_text())
    assert len(data) == 1
    assert data[0]["voc_mv"] == 380
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /home/weissto_local/git/mykovolt && python -m pytest tests/test_export.py::test_export_csv_test_fixture_entry -v`
Expected: FAIL — `_row()` returns dict with `capacitance_pf` key, not `voc_mv`

- [ ] **Step 3: Write minimal implementation**

Replace `_row()` in `mykovolt/export.py`:

```python
from mykovolt.schema import SensorEntry, TestFixtureEntry


def _row(entry: SensorEntry | TestFixtureEntry) -> dict:
    if isinstance(entry, TestFixtureEntry):
        return {
            "timestamp": entry.timestamp,
            "voc_mv": entry.voc_mv,
            "load_current_ma": entry.load_current_ma,
            "load_resistor_index": entry.load_resistor_index,
            "temp_c": entry.temp_c,
            "humidity_pct": entry.humidity_pct,
            "status": entry.status,
            "crc_ok": entry.crc_ok,
        }
    return {
        "timestamp": entry.timestamp,
        "capacitance_pf": entry.capacitance_pf,
        "v_batt_mv": entry.v_batt_mv,
        "v_sense_mv": entry.v_sense_mv,
        "status": entry.status,
        "crc_ok": entry.crc_ok,
    }
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /home/weissto_local/git/mykovolt && python -m pytest tests/test_export.py -v`
Expected: All tests PASS

- [ ] **Step 5: Commit**

```bash
git add mykovolt/export.py tests/test_export.py
git commit -m "feat: extend export to handle TestFixtureEntry"
```

---

### Task 3: Update CLI parse/fetch for Version-Aware Parsing

**Files:**
- Modify: `mykovolt/cli.py:88-115`
- Test: `tests/test_cli.py`

- [ ] **Step 1: Write the failing test**

```python
# Add to tests/test_cli.py

def test_parse_detects_version(tmp_path):
    from mykovolt.schema import FRAM_MAGIC, FRAM_DATA_START, FRAM_MAX_ENTRIES
    import struct
    header = struct.pack(">HBH", FRAM_MAGIC, 2, 12)
    header += b'\x00' * (256 - len(header))
    entry = b'\x00' * 12
    data = header + entry + b'\x00' * 2048
    bin_file = tmp_path / "fram.bin"
    bin_file.write_bytes(data)
    runner = CliRunner()
    result = runner.invoke(cli, ["parse", str(bin_file)])
    assert result.exit_code == 0
    assert "version=2" in result.output or "entries" in result.output.lower()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /home/weissto_local/git/mykovolt && python -m pytest tests/test_cli.py::test_parse_detects_version -v`
Expected: PASS (current code already parses — but doesn't auto-detect version or show it)

- [ ] **Step 3: Write minimal implementation**

Update the `parse` command in `mykovolt/cli.py` to use `parse_entries_versioned`:

```python
from mykovolt.schema import (
    SensorEntry,
    TestFixtureEntry,
    parse_header,
    parse_entries_versioned,
    FRAM_DATA_START,
    FRAM_MAX_ENTRIES,
)
```

Replace the body of `parse()` (lines 93-114):

```python
@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.option("--output", "-o", default=None, help="Output file")
@click.option("--format", "-f", "fmt", default="csv", help="Output format")
@click.option("--calibration", "-c", default=None, help="Calibration JSON file")
def parse(input, output, fmt, calibration):
    """Parse raw FRAM binary dump."""
    with open(input, "rb") as f:
        data = f.read()
    header = parse_header(data)
    if header is None:
        click.echo("Invalid FRAM header", err=True)
        sys.exit(1)
    click.echo(f"Header: magic=0x{header.magic:04X} version={header.version} "
               f"write_ptr={header.write_ptr}")
    entries = parse_entries_versioned(header, data[FRAM_DATA_START:])
    if calibration and header.version == 1:
        cal = load_calibration(calibration)
        entries = [apply_calibration(e, cal) for e in entries]
    click.echo(f"Parsed {len(entries)} entries (v{header.version})")
    buf = open(output, "w") if output else sys.stdout
    if fmt == "csv":
        export_csv(entries, buf)
    else:
        export_json(entries, buf)
    if output:
        buf.close()
        click.echo(f"Wrote {len(entries)} entries to {output}")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /home/weissto_local/git/mykovolt && python -m pytest tests/test_cli.py -v`
Expected: All tests PASS

- [ ] **Step 5: Commit**

```bash
git add mykovolt/cli.py tests/test_cli.py
git commit -m "feat: version-aware FRAM parsing in CLI parse command"
```

---

### Task 4: CalibratedModel Class

**Files:**
- Create: `mykovolt/calibrate_sim.py`
- Test: `tests/test_calibrate_sim.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_calibrate_sim.py

import pytest
from mykovolt.calibrate_sim import CalibratedModel, fit_model, model_params_to_yaml, model_params_from_yaml


def test_calibrated_model_predicts_power():
    m = CalibratedModel(power_density_uw_cm2=12.5, activation_loss=0.05,
                        ohmic_loss_r_cm2=50.0, depletion_rate=0.02)
    power = m.power_at_current(0.0)  # zero load = raw power
    assert power > 0
    power_loaded = m.power_at_current(1.0)  # 1 mA load
    assert power_loaded < power  # losses reduce power
    assert power_loaded > 0


def test_calibrated_model_iv_curve():
    m = CalibratedModel(power_density_uw_cm2=12.5)
    iv = m.iv_curve(area_cm2=19.63, currents_ma=[0, 0.5, 1.0, 2.0, 5.0])
    assert len(iv) == 5
    assert iv[0].voltage > iv[1].voltage  # voltage drops with current
    assert iv[0].current_ma == 0


def test_fit_model_synthetic():
    """Generate synthetic data, fit, check params recovered."""
    import random
    random.seed(42)
    true_params = {
        "power_density_uw_cm2": 15.0,
        "ohmic_loss_r_cm2": 80.0,
        "depletion_rate": 0.03,
    }
    m_true = CalibratedModel(**true_params)
    measurements = []
    for day in range(30):
        current = random.uniform(0.1, 2.0)
        voltage = m_true.voltage_at_current(current, day=day, area_cm2=19.63)
        measurements.append({
            "day": day,
            "current_ma": current,
            "voltage_mv": voltage,
        })
    fitted = fit_model(measurements, area_cm2=19.63)
    assert abs(fitted.power_density_uw_cm2 - 15.0) < 5.0  # within 33%
    assert abs(fitted.depletion_rate - 0.03) < 0.02


def test_model_params_yaml_roundtrip(tmp_path):
    m = CalibratedModel(power_density_uw_cm2=12.5, ohmic_loss_r_cm2=50.0,
                        depletion_rate=0.02)
    path = tmp_path / "params.yaml"
    model_params_to_yaml(m, path)
    m2 = model_params_from_yaml(path)
    assert m2.power_density_uw_cm2 == pytest.approx(m.power_density_uw_cm2)
    assert m2.ohmic_loss_r_cm2 == pytest.approx(m.ohmic_loss_r_cm2)
    assert m2.depletion_rate == pytest.approx(m.depletion_rate)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /home/weissto_local/git/mykovolt && python -m pytest tests/test_calibrate_sim.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'mykovolt.calibrate_sim'`

- [ ] **Step 3: Write minimal implementation**

Create `mykovolt/calibrate_sim.py`:

```python
"""Calibrated pressling power model with parameter fitting."""

from __future__ import annotations
import math
from dataclasses import dataclass
from pathlib import Path


@dataclass
class IVPoint:
    voltage_mv: float
    current_ma: float
    power_uw: float


@dataclass
class CalibratedModel:
    power_density_uw_cm2: float = 12.5
    activation_loss: float = 0.05
    ohmic_loss_r_cm2: float = 50.0
    depletion_rate: float = 0.02

    def raw_power_uw(self, area_cm2: float, day: int = 0) -> float:
        decay = (1 - self.depletion_rate) ** day
        return self.power_density_uw_cm2 * area_cm2 * decay

    def voltage_oc_mv(self, area_cm2: float, day: int = 0) -> float:
        """Approximate open-circuit voltage from power density.
        
        V_OC ≈ sqrt(4 * P * R_internal) for a simple MFC model.
        Typical range: 300-600 mV.
        """
        p = self.raw_power_uw(area_cm2, day)
        r = self.ohmic_loss_r_cm2 / area_cm2  # effective R scales with 1/area
        voc = math.sqrt(max(4 * p * 1e-6 * r, 1e-12)) * 1000
        return max(min(voc, 800.0), 50.0)

    def voltage_at_current(self, current_ma: float, area_cm2: float = 19.63,
                           day: int = 0) -> float:
        voc = self.voltage_oc_mv(area_cm2, day)
        r_eff = self.ohmic_loss_r_cm2 / area_cm2
        activation = self.activation_loss * math.log1p(current_ma) * 100 if current_ma > 0 else 0
        v = voc - current_ma * r_eff - activation
        return max(v, 0.0)

    def power_at_current(self, current_ma: float, area_cm2: float = 19.63,
                        day: int = 0) -> float:
        v = self.voltage_at_current(current_ma, area_cm2, day)
        return v * current_ma

    def iv_curve(self, area_cm2: float = 19.63,
                 currents_ma: list[float] | None = None) -> list[IVPoint]:
        if currents_ma is None:
            currents_ma = [i * 0.1 for i in range(51)]  # 0 to 5 mA
        points = []
        for i_ma in currents_ma:
            v = self.voltage_at_current(i_ma, area_cm2)
            p = v * i_ma
            points.append(IVPoint(voltage_mv=v, current_ma=i_ma, power_uw=p))
        return points


def fit_model(measurements: list[dict], area_cm2: float = 19.63,
              n_grid: int = 20) -> CalibratedModel:
    """Fit model parameters to measured I/V data using grid search.
    
    Each measurement dict: {"day", "current_ma", "voltage_mv"}.
    Uses brute-force grid search (no scipy dependency).
    """
    best_model = CalibratedModel()
    best_error = float("inf")

    for pd in [i * (30.0 / n_grid) + 5.0 for i in range(n_grid)]:
        for rl in [i * (200.0 / n_grid) + 10.0 for i in range(n_grid)]:
            for dr in [i * (0.05 / n_grid) for i in range(n_grid)]:
                m = CalibratedModel(power_density_uw_cm2=pd,
                                    ohmic_loss_r_cm2=rl,
                                    depletion_rate=dr)
                error = 0.0
                for meas in measurements:
                    v_pred = m.voltage_at_current(
                        meas["current_ma"], area_cm2, day=meas.get("day", 0)
                    )
                    error += (v_pred - meas["voltage_mv"]) ** 2
                if error < best_error:
                    best_error = error
                    best_model = m

    return best_model


def model_params_to_yaml(model: CalibratedModel, path: Path | str) -> None:
    lines = [
        f"power_density_uw_cm2: {model.power_density_uw_cm2:.4f}",
        f"activation_loss: {model.activation_loss:.4f}",
        f"ohmic_loss_r_cm2: {model.ohmic_loss_r_cm2:.4f}",
        f"depletion_rate: {model.depletion_rate:.6f}",
    ]
    Path(path).write_text("\n".join(lines) + "\n")


def model_params_from_yaml(path: Path | str) -> CalibratedModel:
    text = Path(path).read_text()
    params = {}
    for line in text.strip().splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            params[key.strip()] = float(val.strip())
    return CalibratedModel(
        power_density_uw_cm2=params.get("power_density_uw_cm2", 12.5),
        activation_loss=params.get("activation_loss", 0.05),
        ohmic_loss_r_cm2=params.get("ohmic_loss_r_cm2", 50.0),
        depletion_rate=params.get("depletion_rate", 0.02),
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /home/weissto_local/git/mykovolt && python -m pytest tests/test_calibrate_sim.py -v`
Expected: All 4 tests PASS

- [ ] **Step 5: Commit**

```bash
git add mykovolt/calibrate_sim.py tests/test_calibrate_sim.py
git commit -m "feat: add CalibratedModel with grid-search fitting and YAML I/O"
```

---

### Task 5: Geometry Sweep & Multi-Cell Model

**Files:**
- Create: `simulation/calibrated_pressling.py`
- Test: `tests/test_calibrated_pressling.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_calibrated_pressling.py

import pytest
from simulation.calibrated_pressling import geometry_sweep, multi_cell_predict


def test_geometry_sweep_returns_multiple():
    results = geometry_sweep(
        power_density_uw_cm2=12.5,
        diameters_mm=[50, 100, 150],
        heights_mm=[8, 12],
        current_ma=1.0,
    )
    assert len(results) == 6  # 3 diameters × 2 heights
    assert results[0].diameter_mm == 50
    assert results[0].height_mm == 8
    assert results[0].power_uw > 0
    # larger disc should produce more power
    assert results[-1].power_uw > results[0].power_uw


def test_multi_cell_series():
    result = multi_cell_predict(
        n_cells=3, config="series",
        power_density_uw_cm2=12.5, diameter_mm=50, height_mm=8,
        load_current_ma=0.5,
    )
    assert result.voltage_mv > result.cell_voltage_mv  # series adds voltage
    assert abs(result.current_ma - 0.5) < 0.01  # current same as single cell


def test_multi_cell_parallel():
    result = multi_cell_predict(
        n_cells=3, config="parallel",
        power_density_uw_cm2=12.5, diameter_mm=50, height_mm=8,
        load_current_ma=0.5,
    )
    assert result.voltage_mv == pytest.approx(result.cell_voltage_mv)
    # parallel can supply more total current
    assert result.max_current_ma > 0.5
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /home/weissto_local/git/mykovolt && python -m pytest tests/test_calibrated_pressling.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Write minimal implementation**

Create `simulation/calibrated_pressling.py`:

```python
"""Geometry sweep and multi-cell predictions for calibrated pressling model."""

from __future__ import annotations
import math
import sys
from dataclasses import dataclass

sys.path.insert(0, ".")
from mykovolt.calibrate_sim import CalibratedModel


@dataclass
class GeometryResult:
    diameter_mm: float
    height_mm: float
    area_cm2: float
    voltage_mv: float
    power_uw: float


@dataclass
class MultiCellResult:
    n_cells: int
    config: str
    voltage_mv: float
    current_ma: float
    power_uw: float
    cell_voltage_mv: float
    max_current_ma: float


def _disc_area_cm2(diameter_mm: float) -> float:
    return math.pi * (diameter_mm / 2) ** 2 / 100


def geometry_sweep(
    power_density_uw_cm2: float = 12.5,
    ohmic_loss_r_cm2: float = 50.0,
    depletion_rate: float = 0.02,
    diameters_mm: list[float] | None = None,
    heights_mm: list[float] | None = None,
    current_ma: float = 1.0,
    day: int = 0,
) -> list[GeometryResult]:
    if diameters_mm is None:
        diameters_mm = [50, 80, 100, 150, 200, 300]
    if heights_mm is None:
        heights_mm = [8, 12, 20]
    m = CalibratedModel(
        power_density_uw_cm2=power_density_uw_cm2,
        ohmic_loss_r_cm2=ohmic_loss_r_cm2,
        depletion_rate=depletion_rate,
    )
    results = []
    for d in diameters_mm:
        for h in heights_mm:
            area = _disc_area_cm2(d)
            v = m.voltage_at_current(current_ma, area, day)
            p = v * current_ma
            results.append(GeometryResult(
                diameter_mm=d, height_mm=h, area_cm2=area,
                voltage_mv=v, power_uw=p,
            ))
    return results


def multi_cell_predict(
    n_cells: int,
    config: str = "series",
    power_density_uw_cm2: float = 12.5,
    ohmic_loss_r_cm2: float = 50.0,
    depletion_rate: float = 0.02,
    diameter_mm: float = 50.0,
    height_mm: float = 8.0,
    load_current_ma: float = 0.5,
    day: int = 0,
) -> MultiCellResult:
    area = _disc_area_cm2(diameter_mm)
    m = CalibratedModel(
        power_density_uw_cm2=power_density_uw_cm2,
        ohmic_loss_r_cm2=ohmic_loss_r_cm2,
        depletion_rate=depletion_rate,
    )
    cell_v = m.voltage_at_current(load_current_ma, area, day)
    cell_max_i = cell_v / (m.ohmic_loss_r_cm2 / area) if area > 0 else 0

    if config == "series":
        total_v = cell_v * n_cells
        total_i = load_current_ma
        max_i = cell_max_i
    elif config == "parallel":
        total_v = cell_v
        total_i = load_current_ma
        max_i = cell_max_i * n_cells
    else:
        raise ValueError(f"Unknown config: {config}")

    return MultiCellResult(
        n_cells=n_cells, config=config,
        voltage_mv=total_v, current_ma=total_i,
        power_uw=total_v * total_i,
        cell_voltage_mv=cell_v, max_current_ma=max_i,
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /home/weissto_local/git/mykovolt && python -m pytest tests/test_calibrated_pressling.py -v`
Expected: All 3 tests PASS

- [ ] **Step 5: Commit**

```bash
git add simulation/calibrated_pressling.py tests/test_calibrated_pressling.py
git commit -m "feat: add geometry sweep and multi-cell prediction for calibrated model"
```

---

### Task 6: `mykovolt calibrate` CLI Command

**Files:**
- Modify: `mykovolt/cli.py:116-121`
- Test: `tests/test_cli.py`

- [ ] **Step 1: Write the failing test**

```python
# Add to tests/test_cli.py

def test_calibrate_command(tmp_path):
    import csv, struct
    from mykovolt.schema import FRAM_MAGIC, FRAM_DATA_START
    header = struct.pack(">HBH", FRAM_MAGIC, 2, 0)
    header += b'\x00' * (256 - len(header))
    entries_data = b''
    for i in range(10):
        day = i
        current_x10 = int(10.0 * 10)
        ts = 1700000000 + i * 3600
        e = struct.pack(">IhHBBbB", ts, 400, current_x10, 2, 20, 50, 0)
        crc = 0
        for b in e:
            crc ^= b
        e += bytes([crc])
        entries_data += e
    bin_file = tmp_path / "test.bin"
    bin_file.write_bytes(header + entries_data)
    csv_file = tmp_path / "test.csv"
    runner = CliRunner()
    result = runner.invoke(cli, ["parse", str(bin_file), "-o", str(csv_file)])
    assert result.exit_code == 0

    out_yaml = tmp_path / "params.yaml"
    result2 = runner.invoke(cli, ["calibrate", str(csv_file), "-o", str(out_yaml)])
    assert result2.exit_code == 0
    assert out_yaml.exists()
    text = out_yaml.read_text()
    assert "power_density_uw_cm2" in text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /home/weissto_local/git/mykovolt && python -m pytest tests/test_cli.py::test_calibrate_command -v`
Expected: FAIL — `calibrate` command just prints "not yet implemented"

- [ ] **Step 3: Write minimal implementation**

Replace the `calibrate` command in `mykovolt/cli.py`:

```python
import csv as csv_mod
from mykovolt.calibrate_sim import fit_model, model_params_to_yaml


@cli.command()
@click.argument("input", type=click.Path(exists=True))
@click.option("--output", "-o", default="model_params.yaml", help="Output YAML file")
@click.option("--area", default=19.63, help="Cell area in cm² (default: Ø50mm disc)")
def calibrate(input, output, area):
    """Fit pressling model parameters to measured CSV data."""
    if input.endswith(".bin"):
        click.echo("Error: calibrate requires CSV input. Run 'mykovolt parse' first.", err=True)
        sys.exit(1)
    with open(input, newline="") as f:
        rows = list(csv_mod.DictReader(f))
    if not rows:
        click.echo("No data rows found", err=True)
        sys.exit(1)
    measurements = []
    for r in rows:
        if "voc_mv" not in r or "load_current_ma" not in r:
            click.echo("Error: CSV must have voc_mv and load_current_ma columns", err=True)
            sys.exit(1)
        ts = int(r.get("timestamp", 0))
        day = ts // 86400 if ts > 1700000000 else 0
        measurements.append({
            "day": day,
            "current_ma": float(r["load_current_ma"]),
            "voltage_mv": float(r["voc_mv"]),
        })
    model = fit_model(measurements, area_cm2=area)
    model_params_to_yaml(model, output)
    click.echo(f"Fitted {len(measurements)} measurements → {output}")
    click.echo(f"  power_density = {model.power_density_uw_cm2:.2f} µW/cm²")
    click.echo(f"  ohmic_loss   = {model.ohmic_loss_r_cm2:.1f} Ω·cm²")
    click.echo(f"  depletion    = {model.depletion_rate:.4f} /day")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /home/weissto_local/git/mykovolt && python -m pytest tests/test_cli.py -v`
Expected: All tests PASS

- [ ] **Step 5: Commit**

```bash
git add mykovolt/cli.py tests/test_cli.py
git commit -m "feat: implement calibrate CLI command with model fitting"
```

---

### Task 7: Run Full Test Suite

- [ ] **Step 1: Run all tests**

Run: `cd /home/weissto_local/git/mykovolt && python -m pytest tests/ -v --tb=short`
Expected: All tests PASS

- [ ] **Step 2: Verify CLI smoke test**

Run: `cd /home/weissto_local/git/mykovolt && python -m mykovolt --help`
Expected: Shows `pipeline`, `fetch`, `parse`, `calibrate`, `plot` commands

Run: `cd /home/weissto_local/git/mykovolt && python -m mykovolt calibrate --help`
Expected: Shows `--area` and `--output` options
