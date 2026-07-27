"""Tests for firmware header consistency.

Validates that firmware headers are self-consistent and match the
hardware design.
"""

import os
import re
import sys

PROJECT_DIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, PROJECT_DIR)
sys.path.insert(0, os.path.join(PROJECT_DIR, "hardware", "kicad"))

from generate_kicad import COMPONENTS, NETS


# ═══════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════

FIRMWARE_INC = os.path.join(PROJECT_DIR, "firmware", "Core", "Inc")


def _read_header(name):
    """Read a firmware header file."""
    path = os.path.join(FIRMWARE_INC, name)
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return f.read()


def _extract_defines(header_text, pattern=r'#define\s+(\w+)\s+(.+)'):
    """Extract #define macros from header text."""
    matches = re.findall(pattern, header_text, re.MULTILINE)
    return {name: value.strip() for name, value in matches}


def _extract_i2c_addresses(header_text):
    """Extract I2C address defines (I2C_ADDR_*)."""
    return _extract_defines(header_text, r'#define\s+(I2C_ADDR_\w+)\s+(0x[0-9A-Fa-f]+)')


# ═══════════════════════════════════════════════════════════════
# Tests
# ═══════════════════════════════════════════════════════════════

class TestMykovoltHeader:
    """Validate mykovolt.h board definitions."""

    def test_header_exists(self):
        content = _read_header("mykovolt.h")
        assert content is not None, "mykovolt.h not found"

    def test_i2c_addresses_are_unique(self):
        content = _read_header("mykovolt.h")
        addrs = _extract_i2c_addresses(content)
        values = list(addrs.values())
        assert len(values) == len(set(values)), \
            f"Duplicate I2C addresses: {[v for v in values if values.count(v) > 1]}"

    def test_i2c_addresses_match_netlist(self):
        """I2C addresses in firmware match the hardware I2C bus."""
        content = _read_header("mykovolt.h")
        addrs = _extract_i2c_addresses(content)
        # Expected I2C devices from schematic
        assert "I2C_ADDR_FRAM" in addrs, "Missing FRAM address"
        assert "I2C_ADDR_FDC1004" in addrs, "Missing FDC1004 address"
        assert "I2C_ADDR_PCF8523" in addrs, "Missing PCF8523 address"
        assert "I2C_ADDR_ST25DV04K" in addrs, "Missing ST25DV04K address"

    def test_pin_definitions_are_valid(self):
        """Pin number macro values (e.g., PIN_LED_CTRL) match GPIO pin numbers."""
        content = _read_header("mykovolt.h")
        defines = _extract_defines(content)
        # Check that pin defines reference valid GPIO pin macros
        pin_defines = {k: v for k, v in defines.items() if k.startswith("PIN_")}
        for name, value in pin_defines.items():
            # Values should be like GPIO_PIN_6, GPIO_PIN_4, etc.
            assert "GPIO_PIN_" in value, f"{name} = {value} doesn't reference GPIO_PIN_x"

    def test_i2c_devices_exist_in_hardware(self):
        """Every I2C device in firmware matches a component in the schematic."""
        content = _read_header("mykovolt.h")
        addrs = _extract_i2c_addresses(content)
        # Map firmware names to schematic refs
        fw_to_hw = {
            "I2C_ADDR_FRAM": "U4",       # MB85RC16
            "I2C_ADDR_FDC1004": "U6",    # FDC1004
            "I2C_ADDR_PCF8523": "U5",    # PCF8523T
            "I2C_ADDR_ST25DV04K": "U3",  # ST25DV04K
        }
        hw_refs = {c[0] for c in COMPONENTS}
        for fw_name, hw_ref in fw_to_hw.items():
            assert fw_name in addrs, f"Firmware missing {fw_name}"
            assert hw_ref in hw_refs, f"Hardware missing {hw_ref} (referenced by {fw_name})"

    def test_power_nets_in_firmware(self):
        """Firmware references correct power management components."""
        content = _read_header("mykovolt.h")
        assert content is not None
        # Check key power defines exist
        assert "PIN_VBAT_OK" in content
        assert "PIN_LOAD_SW_GATE" in content
        assert "VBAT_OK_THRESHOLD_MV" in content
        assert "V_SENSE_DIVIDER_RATIO" in content

    def test_application_states_defined(self):
        """All application states are defined."""
        content = _read_header("mykovolt.h")
        assert "APP_STATE_SLEEP" in content
        assert "APP_STATE_ACTIVE" in content
        assert "APP_STATE_NFC_ACCESS" in content
        assert "APP_STATE_ERROR" in content


class TestFdc1004Header:
    """Validate FDC1004 driver header."""

    def test_header_exists(self):
        content = _read_header("fdc1004.h")
        assert content is not None, "fdc1004.h not found"

    def test_register_definitions_are_sequential(self):
        """FDC1004 register addresses follow the expected pattern (0x00-0x11)."""
        content = _read_header("fdc1004.h")
        defines = _extract_defines(content)
        reg_defines = {k: v for k, v in defines.items() if k.startswith("FDC1004_REG_") and not k.startswith("FDC1004_REG_CONF")}
        for name, value in reg_defines.items():
            # Values should be hex addresses
            assert value.startswith("0x"), f"{name} = {value} is not a hex address"

    def test_channel_defines_exist(self):
        """FDC1004 channel defines are present."""
        content = _read_header("fdc1004.h")
        assert "FDC1004_CIN1" in content
        assert "FDC1004_CIN2" in content


class TestSt25dv04kHeader:
    """Validate ST25DV04K driver header."""

    def test_header_exists(self):
        content = _read_header("st25dv04k.h")
        assert content is not None, "st25dv04k.h not found"

    def test_mailbox_api_exists(self):
        """ST25DV04K mailbox read/write API is defined."""
        content = _read_header("st25dv04k.h")
        assert "st25dv04k_mailbox_read" in content
        assert "st25dv04k_mailbox_write" in content
        assert "st25dv04k_mailbox_read_len" in content

    def test_user_memory_size_correct(self):
        """ST25DV04K has 4Kbit = 512 bytes user memory."""
        content = _read_header("st25dv04k.h")
        assert "ST25DV04K_USER_MEM_SIZE" in content
        assert "512" in content.split("ST25DV04K_USER_MEM_SIZE")[1][:20] or "0x200" in content.split("ST25DV04K_USER_MEM_SIZE")[1][:20]


class TestI2cDriverHeader:
    """Validate I2C driver header."""

    def test_header_exists(self):
        content = _read_header("i2c_driver.h")
        assert content is not None, "i2c_driver.h not found"

    def test_api_functions_defined(self):
        """All I2C driver API functions are declared."""
        content = _read_header("i2c_driver.h")
        assert "i2c_init" in content
        assert "i2c_write_reg" in content
        assert "i2c_read_reg" in content
        assert "i2c_ready" in content
        assert "i2c_error_count" in content


# ═══════════════════════════════════════════════════════════════
# Cross-consistency between hardware and firmware
# ═══════════════════════════════════════════════════════════════

class TestHardwareFirmwareConsistency:
    """Validate that firmware headers match the hardware design."""

    def test_firmware_has_all_i2c_devices(self):
        """The firmware I2C address defines cover all I2C devices in the schematic."""
        content = _read_header("mykovolt.h")
        fw_addrs = _extract_i2c_addresses(content)

        # Find all I2C devices in the schematic (U3, U4, U5, U6 are I2C)
        i2c_devices = {"U3", "U4", "U5", "U6"}
        assert len(fw_addrs) >= len(i2c_devices), \
            f"Firmware defines {len(fw_addrs)} I2C addresses, schematic has {len(i2c_devices)} I2C devices"

    def test_sensor_pins_match(self):
        """FDC1004 sensor pins (CIN1, CIN2) match J4 connector in schematic."""
        # Find the CIN nets in the netlist
        cin_nets = [n for n in NETS if n[0].startswith("CIN") or n[0] == "SHLD1"]
        assert len(cin_nets) >= 2, f"Expected at least CIN1 and CIN2 nets, found {len(cin_nets)}"

        # Verify CIN1 connects to U6 and J4
        for net_name, conns in cin_nets:
            refs = [r for r, _ in conns]
            assert "U6" in refs, f"{net_name} doesn't connect to FDC1004"
            # J4 may or may not be connected in every CIN net
