import struct
from mykovolt.schema import RingBufferHeader, SensorEntry, parse_header, parse_entries


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
