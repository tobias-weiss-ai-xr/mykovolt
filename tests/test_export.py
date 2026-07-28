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
