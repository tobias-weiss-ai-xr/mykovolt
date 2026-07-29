/**
 * @file    sht30.h
 * @brief   SHT30 temperature + humidity sensor driver (I2C)
 *
 * Datasheet: Sensirion SHT30, Digital Humidity and Temperature Sensor
 * Protocol:  7-bit addr 0x44, command-based (2-byte commands, no register addressing)
 */

#ifndef __SHT30_H
#define __SHT30_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>

/* ── Commands ── */

/* Single-shot mode, clock stretching enabled, high repeatability */
#define SHT30_CMD_SINGLESHOT_H   0x2C06
/* Single-shot mode, clock stretching enabled, medium repeatability */
#define SHT30_CMD_SINGLESHOT_M   0x2C0D
/* Single-shot mode, clock stretching enabled, low repeatability */
#define SHT30_CMD_SINGLESHOT_L   0x2C10
/* Soft reset */
#define SHT30_CMD_SOFT_RESET     0x30A2
/* Read status register */
#define SHT30_CMD_READ_STATUS    0xF32D

/* ── Public API ── */

/** Initialise SHT30 (soft reset + verify status register) */
bool sht30_init(void);

/**
 * Read temperature and humidity (blocking, ~15ms conversion time).
 * @param temp_c  Output: temperature in degrees Celsius (signed, -40 to +125)
 * @param rh_pct  Output: relative humidity in percent (0 to 100)
 * @return true on success, false on I2C/CRC error
 */
bool sht30_read(int8_t *temp_c, uint8_t *rh_pct);

uint8_t sht30_crc8(const uint8_t *data, uint8_t len);

#ifdef __cplusplus
}
#endif

#endif /* __SHT30_H */
