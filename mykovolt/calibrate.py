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
