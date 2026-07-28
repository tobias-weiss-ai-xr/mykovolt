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
