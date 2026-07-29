import json
import pytest
from mykovolt.schema import SensorEntry
from mykovolt.calibrate import Calibration, load_calibration, apply_calibration


def test_load_calibration(tmp_path):
    cal_file = tmp_path / "cal.json"
    cal_file.write_text(
        json.dumps(
            [
                {"channel": "CIN1", "offset_pf": 0.5, "gain": 1.02},
            ]
        )
    )
    cal = load_calibration(str(cal_file))
    assert cal.offsets.get("CIN1", 0.0) == 0.5
    assert cal.gains.get("CIN1", 1.0) == 1.02


def test_calibration_file_not_found():
    cal = load_calibration("/nonexistent/cal.json")
    assert len(cal.offsets) == 0


def test_apply_calibration_default():
    entry = SensorEntry(1000, 123.45, 3100, 1500, 0x01, True)
    cal = Calibration()
    result = apply_calibration(entry, cal)
    assert abs(result.capacitance_pf - 123.45) < 0.01


def test_apply_calibration_with_offset_gain():
    entry = SensorEntry(1000, 123.45, 3100, 1500, 0x01, True)
    cal = Calibration(offsets={"CIN1": -0.5}, gains={"CIN1": 1.05})
    result = apply_calibration(entry, cal)
    expected = (123.45 - 0.5) * 1.05
    assert abs(result.capacitance_pf - expected) < 0.01
