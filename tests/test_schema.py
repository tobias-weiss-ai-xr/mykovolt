import struct
import pytest
from mykovolt.schema import (
    RingBufferHeader,
    SensorEntry,
    TestFixtureEntry,
    parse_header,
    parse_entries,
    parse_entries_versioned,
)


def test_parse_header_valid():
    data = struct.pack(">HBH", 0x4D56, 0x01, 0x0018)
    data += b"\x00" * 251
    hdr = parse_header(data)
    assert hdr.magic == 0x4D56
    assert hdr.version == 0x01
    assert hdr.write_ptr == 24


def test_parse_header_invalid_magic():
    data = struct.pack(">HBH", 0x0000, 0x01, 0x0000)
    data += b"\x00" * 251
    assert parse_header(data) is None


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
    raw += bytes([crc ^ 0xFF])
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


def test_test_fixture_entry_from_bytes():
    payload = struct.pack(
        ">IHhBbBB",
        1750000000,  # timestamp (uint32)
        380,  # voc_mv (uint16, 0.38V)
        250,  # load_current_ma (int16, raw mA)
        2,  # load_resistor_index (uint8, R2)
        22,  # temperature_c (int8)
        65,  # humidity_pct (uint8)
        0x01,  # status (uint8)
    )
    assert len(payload) == 12
    crc = 0
    for b in payload:
        crc ^= b
    data = payload + bytes([crc])
    assert len(data) == 13

    entry = TestFixtureEntry.from_bytes(data)
    assert entry.timestamp == 1750000000
    assert entry.voc_mv == 380
    assert entry.load_current_ma == 250
    assert entry.load_resistor_index == 2
    assert entry.temp_c == 22
    assert entry.humidity_pct == 65
    assert entry.status == 0x01
    assert entry.crc_ok is True


def test_test_fixture_entry_bad_crc():
    data = struct.pack(">IHhBbBB", 0, 0, 0, 0, 0, 0, 0)
    data += bytes([0xFF])  # wrong CRC
    entry = TestFixtureEntry.from_bytes(data)
    assert entry.crc_ok is False


def test_test_fixture_entry_negative_temp():
    """Temperature is signed int8 — supports -40 to +127°C."""
    data = struct.pack(
        ">IHhBbBB",
        0,  # timestamp
        400,  # voc_mv
        100,  # load_current_ma (raw, signed)
        1,  # load_resistor_index
        -10,  # temp_c (signed)
        80,  # humidity (unsigned)
        0,  # status
    )
    crc = 0
    for b in data:
        crc ^= b
    data += bytes([crc])
    assert len(data) == 13

    entry = TestFixtureEntry.from_bytes(data)
    assert entry.temp_c == -10
    assert entry.humidity_pct == 80
    assert entry.load_current_ma == 100


def test_test_fixture_entry_negative_current():
    """Load current is signed int16."""
    data = struct.pack(
        ">IHhBbBB",
        0,
        0,
        -50,  # negative current
        0,
        0,
        0,
        0,
    )
    crc = 0
    for b in data:
        crc ^= b
    data += bytes([crc])
    entry = TestFixtureEntry.from_bytes(data)
    assert entry.load_current_ma == -50


def test_parse_entries_versioned_v1():
    from mykovolt.schema import FRAM_MAGIC

    header_data = struct.pack(">HBH", FRAM_MAGIC, 1, 12) + b"\x00" * 251
    header = parse_header(header_data)
    assert header.version == 1
    entries = parse_entries_versioned(header, b"\x00" * 12)
    assert len(entries) == 1
    assert isinstance(entries[0], SensorEntry)


def test_parse_entries_versioned_v2():
    from mykovolt.schema import FRAM_MAGIC

    header_data = struct.pack(">HBH", FRAM_MAGIC, 2, 13) + b"\x00" * 251
    header = parse_header(header_data)
    assert header.version == 2
    entries = parse_entries_versioned(header, b"\x00" * 13)
    assert len(entries) == 1
    assert isinstance(entries[0], TestFixtureEntry)


def test_parse_entries_versioned_v2_empty():
    from mykovolt.schema import FRAM_MAGIC, FRAM_ENTRY_SIZE_V2

    header_data = struct.pack(">HBH", FRAM_MAGIC, 2, 0) + b"\x00" * 251
    header = parse_header(header_data)
    entries = parse_entries_versioned(header, b"\x00" * 100)
    assert entries == []


def test_parse_entries_versioned_v2_multiple():
    from mykovolt.schema import FRAM_MAGIC, FRAM_ENTRY_SIZE_V2

    header_data = (
        struct.pack(">HBH", FRAM_MAGIC, 2, FRAM_ENTRY_SIZE_V2 * 3) + b"\x00" * 251
    )
    header = parse_header(header_data)
    data = b"\x00" * (FRAM_ENTRY_SIZE_V2 * 5)
    entries = parse_entries_versioned(header, data)
    assert len(entries) == 3
    assert all(isinstance(e, TestFixtureEntry) for e in entries)


def test_parse_entries_versioned_unknown_version():
    from mykovolt.schema import FRAM_MAGIC

    header_data = struct.pack(">HBH", FRAM_MAGIC, 99, 12) + b"\x00" * 251
    header = parse_header(header_data)
    with pytest.raises(ValueError, match="version"):
        parse_entries_versioned(header, b"\x00" * 12)
