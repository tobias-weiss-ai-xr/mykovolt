/**
 * @file    sht30.c
 * @brief   SHT30 temperature + humidity sensor driver
 *
 * Datasheet: Sensirion SHT30, Digital Humidity and Temperature Sensor
 *
 * Conversion formulas (from datasheet):
 *   T = -45 + 175 * (S_T / 65535)    [°C, signed]
 *   RH = 100 * (S_RH / 65535)        [%RH, unsigned]
 *
 * CRC-8: polynomial 0x31, initial value 0xFF
 */

#include "sht30.h"
#include "i2c_driver.h"
#include "mykovolt.h"

/* I2C address — defined in testfixture_config.h, fallback for dev kit compatibility */
#ifndef I2C_ADDR_SHT30
#define I2C_ADDR_SHT30 0x44
#endif

/* ======== Private helpers ======== */

static bool send_command(uint16_t cmd) {
    /* Use i2c_write_reg16 with len=0 to send just the 2-byte command */
    return i2c_write_reg16(I2C_ADDR_SHT30, cmd, (const uint8_t *)0, 0);
}

static uint8_t crc8(const uint8_t *data, uint8_t len) {
    uint8_t crc = 0xFF;
    for (uint8_t i = 0; i < len; i++) {
        crc ^= data[i];
        for (uint8_t b = 0; b < 8; b++) {
            if (crc & 0x80) {
                crc = (crc << 1) ^ 0x31;
            } else {
                crc <<= 1;
            }
        }
    }
    return crc;
}

/* ======== Public API ======== */

bool sht30_init(void) {
    /* Soft reset */
    if (!send_command(SHT30_CMD_SOFT_RESET)) {
        return false;
    }
    /* Wait for reset (max 1.5ms per datasheet) */
    for (volatile int i = 0; i < 5000; i++);

    /* Read status register to verify device is alive */
    uint8_t status[3];
    if (!i2c_read_reg16(I2C_ADDR_SHT30, SHT30_CMD_READ_STATUS, status, 3)) {
        return false;
    }
    /* Verify CRC */
    if (crc8(status, 2) != status[2]) {
        return false;
    }
    return true;
}

bool sht30_read(int8_t *temp_c, uint8_t *rh_pct) {
    /* Send single-shot command (clock stretching, high repeatability) */
    if (!send_command(SHT30_CMD_SINGLESHOT_H)) {
        return false;
    }

    /* Read 6 bytes: T_msb, T_lsb, T_crc, RH_msb, RH_lsb, RH_crc */
    uint8_t data[6];
    if (!i2c_read_raw(I2C_ADDR_SHT30, data, 6)) {
        return false;
    }

    /* Verify CRCs */
    if (crc8(data, 2) != data[2]) {
        return false;
    }
    if (crc8(data + 3, 2) != data[5]) {
        return false;
    }

    /* Convert raw values */
    uint16_t raw_t = ((uint16_t)data[0] << 8) | data[1];
    uint16_t raw_rh = ((uint16_t)data[3] << 8) | data[4];

    /* T = -45 + 175 * raw / 65535 → integer math:
     * temp_c = -45 + (175 * raw_t) / 65535
     * To avoid overflow with 32-bit: (175 * raw_t) can be up to 175*65535 = 11,468,625 (fits in 32-bit) */
    int32_t temp_x100 = -4500 + (17500 * (int32_t)raw_t) / 65535;
    /* Round to nearest degree */
    int8_t temp = (int8_t)((temp_x100 + 50) / 100);

    /* RH = 100 * raw / 65535 → integer math:
     * rh = (100 * raw_rh) / 65535, clamped to [0, 100] */
    uint8_t rh = (uint8_t)((100 * raw_rh) / 65535);
    if (rh > 100) rh = 100;

    if (temp_c) *temp_c = temp;
    if (rh_pct) *rh_pct = rh;

    return true;
}
