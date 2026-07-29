from __future__ import annotations
import csv
import json
import io
from typing import TextIO
from mykovolt.schema import SensorEntry, TestFixtureEntry

Entry = SensorEntry | TestFixtureEntry


def _row(entry: Entry) -> dict:
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


def export_csv(entries: list[Entry], buf: TextIO) -> None:
    if not entries:
        return
    writer = csv.DictWriter(buf, fieldnames=list(_row(entries[0]).keys()))
    writer.writeheader()
    for entry in entries:
        writer.writerow(_row(entry))


def export_json(entries: list[Entry], buf: TextIO) -> None:
    json.dump([_row(e) for e in entries], buf, indent=2)


def export_parquet(entries: list[Entry], path: str) -> None:
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
