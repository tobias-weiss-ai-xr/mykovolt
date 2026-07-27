/**
 * @file    fdc1004.h
 * @brief   Driver for TI FDC1004 capacitance sensor
 *
 * 4-channel capacitance-to-digital converter with shield driver.
 * I2C address: 0x51 (ADDR pin = VDD via 10kΩ)
 */

#ifndef __FDC1004_H
#define __FDC1004_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>

/* ── Registers ── */

#define FDC1004_REG_CIN1_MSB    0x00
#define FDC1004_REG_CIN1_LSB    0x01
#define FDC1004_REG_CIN2_MSB    0x02
#define FDC1004_REG_CIN2_LSB    0x03
#define FDC1004_REG_CIN3_MSB    0x04
#define FDC1004_REG_CIN3_LSB    0x05
#define FDC1004_REG_CIN4_MSB    0x06
#define FDC1004_REG_CIN4_LSB    0x07
#define FDC1004_REG_CONF_MSB    0x08
#define FDC1004_REG_CONF_LSB    0x09
#define FDC1004_REG_OFFSET_CIN1 0x0A
#define FDC1004_REG_OFFSET_CIN2 0x0B
#define FDC1004_REG_OFFSET_CIN3 0x0C
#define FDC1004_REG_OFFSET_CIN4 0x0D
#define FDC1004_REG_GAIN_CIN1   0x0E
#define FDC1004_REG_GAIN_CIN2   0x0F
#define FDC1004_REG_GAIN_CIN3   0x10
#define FDC1004_REG_GAIN_CIN4   0x11
#define FDC1004_REG_MANUFACTURER_ID 0xFE
#define FDC1004_REG_DEVICE_ID   0xFF

/* ── Configuration bitfields ── */

#define FDC1004_MEAS_RATE_10HZ   (0 << 8)
#define FDC1004_MEAS_RATE_100HZ  (1 << 8)
#define FDC1004_MEAS_RATE_200HZ  (2 << 8)
#define FDC1004_MEAS_RATE_400HZ  (3 << 8)

#define FDC1004_AMUX_DISABLED    (0 << 13)
#define FDC1004_AMUX_CIN1        (1 << 13)
#define FDC1004_AMUX_CIN2        (2 << 13)
#define FDC1004_AMUX_CIN3        (3 << 13)
#define FDC1004_AMUX_CIN4        (4 << 13)
#define FDC1004_AMUX_CAL_CAP     (5 << 13)
#define FDC1004_AMUX_VDD_DIV2    (6 << 13)
#define FDC1004_AMUX_VDD         (7 << 13)

/* ── Measurement trigger ── */

#define FDC1004_REG_TRIGGER      0x0C  /* Actually 0x0C in some docs; check */
#define FDC1004_TRIGGER_SINGLE   (1 << 15)

/* ── Public API ── */

/** Initialise the FDC1004 (reset, set measurement rate) */
bool fdc1004_init(void);

/** Read raw capacitance from a channel (0-3). Returns femtofarads × 100 */
int32_t fdc1004_read_raw(uint8_t channel);

/** Read capacitance in pF (floating point, slow) */
float fdc1004_read_pf(uint8_t channel);

/** Check if a measurement is complete */
bool fdc1004_is_ready(void);

/** Read the offset calibration register for a channel */
int16_t fdc1004_read_offset(uint8_t channel);

/** Read the gain calibration register for a channel */
uint16_t fdc1004_read_gain(uint8_t channel);

/** Read manufacturer ID (should be 0x5449 = "TI") */
uint16_t fdc1004_read_manufacturer_id(void);

/** Read device ID (should be 0x1004) */
uint16_t fdc1004_read_device_id(void);

/* ── Channel definitions ── */

#define FDC1004_CIN1         0  /* Soil moisture sensor */
#define FDC1004_CIN2         1  /* Reference / compensation */
#define FDC1004_CIN3         2  /* Spare */
#define FDC1004_CIN4         3  /* Not used */

#ifdef __cplusplus
}
#endif

#endif /* __FDC1004_H */
