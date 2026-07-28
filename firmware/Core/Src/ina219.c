/**
 * @file    ina219.c
 * @brief   INA219 current/voltage/power sensor driver
 *
 * Datasheet: Texas Instruments INA219, Zero-Drift Bidirectional
 *            Current/Power Monitor With I2C Interface
 *
 * With 0.1 Ω shunt and default config:
 *   - Bus voltage LSB = 4 mV
 *   - Shunt voltage LSB = 10 µV
 *   - Current = shunt_voltage / R_shunt = (raw × 10 µV) / 0.1 Ω = raw × 100 µA = raw × 0.1 mA
 */

#include "ina219.h"
#include "i2c_driver.h"
#include "mykovolt.h"

/* I2C address — defined in testfixture_config.h, fallback for dev kit compatibility */
#ifndef I2C_ADDR_INA219
#define I2C_ADDR_INA219 0x40
#endif

/* ======== Private helpers ======== */

static uint16_t read_reg_u16(uint8_t reg) {
    uint8_t buf[2];
    if (!i2c_read_reg(I2C_ADDR_INA219, reg, buf, 2)) {
        return 0xFFFF;
    }
    return ((uint16_t)buf[0] << 8) | buf[1];
}

static bool write_reg_u16(uint8_t reg, uint16_t val) {
    uint8_t buf[2];
    buf[0] = (uint8_t)(val >> 8);
    buf[1] = (uint8_t)(val);
    return i2c_write_reg(I2C_ADDR_INA219, reg, buf, 2);
}

/* ======== Public API ======== */

bool ina219_init(void) {
    if (!write_reg_u16(INA219_REG_CONFIG, INA219_CONFIG_DEFAULT)) {
        return false;
    }
    /* Verify by reading back config */
    uint16_t cfg = read_reg_u16(INA219_REG_CONFIG);
    if (cfg == 0xFFFF) {
        return false;
    }
    return true;
}

uint16_t ina219_read_voltage_mv(void) {
    uint16_t raw = read_reg_u16(INA219_REG_BUS_VOLT);
    if (raw == 0xFFFF) {
        return 0xFFFF;
    }
    /* Bits [15:3] are the voltage in 4mV steps; bit[1] = CNVR, bit[0] = OVF */
    if (raw & 0x0001) {
        /* Overflow — measurement is invalid */
        return 0xFFFF;
    }
    return (raw >> 3) * 4;
}

int16_t ina219_read_current_ma(void) {
    uint16_t raw = read_reg_u16(INA219_REG_SHUNT_VOLT);
    if (raw == 0xFFFF) {
        return 0x7FFF;
    }
    /* Shunt voltage is signed 16-bit, 10 µV/LSB */
    int16_t shunt_raw = (int16_t)raw;
    /* Current = V_shunt / R_shunt = (shunt_raw × 10 µV) / 0.1 Ω
     *         = shunt_raw × 100 µA = shunt_raw × 0.1 mA
     * So current in mA = shunt_raw / 10 (integer math, 0.1 mA resolution) */
    return shunt_raw / 10;
}

uint16_t ina219_read_power_mw(void) {
    uint16_t v_mv = ina219_read_voltage_mv();
    int16_t i_ma = ina219_read_current_ma();
    if (v_mv == 0xFFFF || i_ma == 0x7FFF) {
        return 0xFFFF;
    }
    if (i_ma < 0) {
        /* Negative current — no power delivered */
        return 0;
    }
    /* Power = V × I / 1000 (mV × mA = µW, /1000 = mW) */
    return (uint16_t)((v_mv * (uint16_t)i_ma) / 1000);
}

bool ina219_conversion_ready(void) {
    uint16_t raw = read_reg_u16(INA219_REG_BUS_VOLT);
    if (raw == 0xFFFF) {
        return false;
    }
    /* Bit [1] of bus voltage register = conversion ready */
    return (raw & 0x0002) != 0;
}
