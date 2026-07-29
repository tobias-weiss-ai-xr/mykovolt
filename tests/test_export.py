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


def test_export_csv_test_fixture_entry(tmp_path):
    from mykovolt.schema import TestFixtureEntry

    entries = [
        TestFixtureEntry(
            timestamp=1000,
            voc_mv=380,
            load_current_ma=250,
            load_resistor_index=2,
            temp_c=22,
            humidity_pct=65,
            status=0,
            crc_ok=True,
        )
    ]
    out = tmp_path / "out.csv"
    with open(out, "w") as f:
        export_csv(entries, f)
    text = out.read_text()
    assert "voc_mv" in text
    assert "380" in text
    assert "250" in text


def test_export_json_test_fixture_entry(tmp_path):
    from mykovolt.schema import TestFixtureEntry

    entries = [
        TestFixtureEntry(
            timestamp=1000,
            voc_mv=380,
            load_current_ma=250,
            load_resistor_index=2,
            temp_c=22,
            humidity_pct=65,
            status=0,
            crc_ok=True,
        )
    ]
    out = tmp_path / "out.json"
    with open(out, "w") as f:
        export_json(entries, f)
    import json

    data = json.loads(out.read_text())
    assert len(data) == 1
    assert data[0]["voc_mv"] == 380
