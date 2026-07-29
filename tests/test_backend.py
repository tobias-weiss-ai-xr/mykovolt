import pytest
from mykovolt.backend import Backend, I2cBackend, NfcBackend


def test_backend_abc_cannot_instantiate():
    with pytest.raises(TypeError):
        Backend()


def test_i2c_backend_read_raises_without_smbus():
    backend = I2cBackend(bus=1, addr=0x50)
    with pytest.raises(RuntimeError, match="smbus2"):
        backend.read(0x00, 10)


def test_nfc_backend_not_implemented():
    backend = NfcBackend()
    with pytest.raises(NotImplementedError):
        backend.read(0x00, 10)


def test_i2c_backend_properties():
    backend = I2cBackend(bus=0, addr=0x51)
    assert backend.bus == 0
    assert backend.addr == 0x51
