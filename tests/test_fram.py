import struct
import pytest
from mykovolt.schema import RingBufferHeader, SensorEntry
from mykovolt.backend import Backend
from mykovolt.fram import read_fram


class MockBackend(Backend):
    def __init__(self, fram_data: bytes):
        self.fram_data = fram_data

    def read(self, addr: int, length: int) -> bytes:
        if addr + length > len(self.fram_data):
            return self.fram_data[addr:]
        return self.fram_data[addr : addr + length]


def make_fram(entries: list[bytes]) -> bytes:
    header = struct.pack(">HBH", 0x4D56, 0x01, len(entries) * 12)
    header = header.ljust(256, b"\x00")
    data = bytearray(header)
    for entry in entries:
        crc = 0
        for b in entry:
            crc ^= b
        data.extend(entry + bytes([crc]))
    return bytes(data)


def test_read_fram_empty():
    data = make_fram([])
    backend = MockBackend(data)
    header, entries = read_fram(backend)
    assert header.magic == 0x4D56
    assert len(entries) == 0


def test_read_fram_three_entries():
    raw_entries = []
    for i in range(3):
        ts = 1000 + i * 60
        raw_entries.append(struct.pack(">IHHHB", ts, 12345, 3100, 1500, 0x01))
    data = make_fram(raw_entries)
    backend = MockBackend(data)
    header, entries = read_fram(backend)
    assert len(entries) == 3


def test_read_fram_corrupt_header():
    data = b"\x00" * 2048
    backend = MockBackend(data)
    with pytest.raises(ValueError, match="magic"):
        read_fram(backend)
