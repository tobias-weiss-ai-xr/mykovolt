"""Read FRAM ring buffer via a Backend."""

from mykovolt.schema import (
    RingBufferHeader,
    SensorEntry,
    parse_header,
    parse_entries,
    FRAM_HEADER_SIZE,
    FRAM_DATA_START,
    FRAM_MAX_ENTRIES,
)
from mykovolt.backend import Backend

FRAM_TOTAL_SIZE = 2048  # MB85RC16 is 16Kbit


def read_fram(backend: Backend) -> tuple[RingBufferHeader, list[SensorEntry]]:
    header_raw = backend.read(0x00, FRAM_HEADER_SIZE)
    header = parse_header(header_raw)
    if header is None:
        raise ValueError("Invalid FRAM magic — device not initialized or wrong backend")
    if header.write_ptr == 0:
        return header, []
    entry_count = min(header.write_ptr // 12, FRAM_MAX_ENTRIES)
    entries_raw = backend.read(FRAM_DATA_START, entry_count * 12)
    entries = parse_entries(entries_raw, entry_count)
    return header, entries
