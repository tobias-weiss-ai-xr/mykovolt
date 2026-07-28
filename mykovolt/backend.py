"""Device communication backends for reading FRAM data."""

from __future__ import annotations
from abc import ABC, abstractmethod


class Backend(ABC):
    @abstractmethod
    def read(self, addr: int, length: int) -> bytes: ...


class I2cBackend(Backend):
    def __init__(self, bus: int = 1, addr: int = 0x50):
        self.bus = bus
        self.addr = addr
        self._dev = None

    def read(self, addr: int, length: int) -> bytes:
        if self._dev is None:
            try:
                import smbus2

                self._dev = smbus2.SMBus(self.bus)
            except ImportError:
                raise RuntimeError("smbus2 not installed. Run: pip install smbus2")
        reg_hi = (addr >> 8) & 0xFF
        reg_lo = addr & 0xFF
        self._dev.write_i2c_block_data(self.addr, reg_hi, [reg_lo])
        return bytes(self._dev.read_i2c_block_data(self.addr, reg_hi, length))


class NfcBackend(Backend):
    def __init__(self):
        self._tag = None

    def read(self, addr: int, length: int) -> bytes:
        raise NotImplementedError("NFC backend requires an NFC reader")
