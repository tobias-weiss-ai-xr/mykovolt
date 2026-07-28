/**
 * @file    mb85rc16.c
 * @brief   MB85RC16 FRAM driver
 *
 * Datasheet: Fujitsu MB85RC16, 16Kbit I2C FRAM
 * Protocol: 7-bit addr 0x50, 16-bit memory address, standard I2C
 * Note:     FRAM needs no write delay (unlike EEPROM), so writes are
 *           immediately available. Only lower 11 address bits are used.
 */

#include "mb85rc16.h"
#include "i2c_driver.h"
#include "mykovolt.h"

/* ── Public API ── */

bool mb85rc16_init(void) {
    /* Verify device presence by reading byte at address 0 */
    uint8_t val = 0;
    if (!i2c_read_reg16(I2C_ADDR_FRAM, 0, &val, 1)) {
        return false;
    }
    return true;
}

uint8_t mb85rc16_read_byte(uint16_t addr) {
    uint8_t val = 0xFF;
    if (addr > MB85RC16_ADDR_MAX) {
        return 0xFF;
    }
    i2c_read_reg16(I2C_ADDR_FRAM, addr, &val, 1);
    return val;
}

uint16_t mb85rc16_read(uint16_t addr, uint8_t *buf, uint16_t len) {
    if (addr > MB85RC16_ADDR_MAX || buf == NULL || len == 0) {
        return 0;
    }
    uint16_t max_read = MB85RC16_SIZE - addr;
    if (len > max_read) {
        len = max_read;
    }
    if (!i2c_read_reg16(I2C_ADDR_FRAM, addr, buf, len)) {
        return 0;
    }
    return len;
}

bool mb85rc16_write_byte(uint16_t addr, uint8_t val) {
    if (addr > MB85RC16_ADDR_MAX) {
        return false;
    }
    return i2c_write_reg16(I2C_ADDR_FRAM, addr, &val, 1);
}

bool mb85rc16_write(uint16_t addr, const uint8_t *data, uint16_t len) {
    if (addr > MB85RC16_ADDR_MAX || data == NULL || len == 0) {
        return false;
    }
    uint16_t max_write = MB85RC16_SIZE - addr;
    if (len > max_write) {
        len = max_write;
    }
    return i2c_write_reg16(I2C_ADDR_FRAM, addr, data, len);
}