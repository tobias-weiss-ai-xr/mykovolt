/**
 * @file    i2c_driver.h
 * @brief   I2C master driver for STM32L011 (bare-metal, no HAL dependency)
 */

#ifndef __I2C_DRIVER_H
#define __I2C_DRIVER_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>

/* ── Initialisation ── */

/** Initialise I2C1 peripheral (PA9=SCL, PA10=SDA, 100kHz standard mode) */
void i2c_init(void);

/** Enable/disable I2C peripheral */
void i2c_enable(void);
void i2c_disable(void);

/* ── Master Transmit ── */

/**
 * Write data to an I2C slave.
 * @param addr  7-bit slave address
 * @param reg   Register address byte
 * @param data  Data buffer
 * @param len   Number of bytes to write
 * @return true on ACK, false on NACK/timeout
 */
bool i2c_write_reg(uint8_t addr, uint8_t reg, const uint8_t *data, uint16_t len);

/**
 * Write a single byte to a register.
 */
static inline bool i2c_write_reg8(uint8_t addr, uint8_t reg, uint8_t val) {
    return i2c_write_reg(addr, reg, &val, 1);
}

/* ── 16-bit register address variants ── */

/**
 * Write data to an I2C slave using a 16-bit register address.
 * Used by devices like ST25DV04K, FRAM with 16-bit address maps.
 */
bool i2c_write_reg16(uint8_t addr, uint16_t reg, const uint8_t *data, uint16_t len);

/**
 * Read data from an I2C slave using a 16-bit register address.
 */
bool i2c_read_reg16(uint8_t addr, uint16_t reg, uint8_t *data, uint16_t len);

/* ── Master Receive ── */

/**
 * Read data from an I2C slave.
 * @param addr  7-bit slave address
 * @param reg   Register address byte
 * @param data  Buffer for received data
 * @param len   Number of bytes to read
 * @return true on ACK, false on NACK/timeout
 */
bool i2c_read_reg(uint8_t addr, uint8_t reg, uint8_t *data, uint16_t len);

/**
 * Read a single byte from a register.
 */
static inline uint8_t i2c_read_reg8(uint8_t addr, uint8_t reg) {
    uint8_t val = 0;
    i2c_read_reg(addr, reg, &val, 1);
    return val;
}

/* ── Raw I2C (no register address) ── */

/**
 * Read data from an I2C slave without sending a register address first.
 * Used by command-based devices like SHT30.
 * @param addr  7-bit slave address
 * @param data  Buffer for received data
 * @param len   Number of bytes to read
 * @return true on ACK, false on NACK/timeout
 */
bool i2c_read_raw(uint8_t addr, uint8_t *data, uint16_t len);

/* ── Status / Debug ── */

/** Check if I2C bus is ready */
bool i2c_ready(void);

/** Return number of bus errors since last init */
uint32_t i2c_error_count(void);

#ifdef __cplusplus
}
#endif

#endif /* __I2C_DRIVER_H */
