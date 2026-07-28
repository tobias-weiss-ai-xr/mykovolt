/**
 * @file    ina219.h
 * @brief   INA219 current/voltage/power sensor driver (I2C)
 *
 * Datasheet: Texas Instruments INA219, I2C 26V/32V Bus Voltage Monitor
 * Protocol:  7-bit addr 0x40 (configurable via A0/A1), 8-bit register addressing
 */

#ifndef __INA219_H
#define __INA219_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>

/* ── Registers ── */

#define INA219_REG_CONFIG       0x00
#define INA219_REG_SHUNT_VOLT   0x01
#define INA219_REG_BUS_VOLT     0x02
#define INA219_REG_POWER        0x03
#define INA219_REG_CURRENT      0x04
#define INA219_REG_CALIBRATION  0x05

/* ── Config defaults ── */

/* 32V range, PGA /8 (±320mV), 12-bit bus+shunt, continuous mode */
#define INA219_CONFIG_DEFAULT   0x399F

/* Shunt resistor in milliohms (0.1 Ω = 100 mΩ) */
#define INA219_SHUNT_MOHM       100

/* ── Public API ── */

/** Initialise INA219 (writes config register, verifies device presence) */
bool ina219_init(void);

/** Read bus voltage in millivolts (returns 0xFFFF on error) */
uint16_t ina219_read_voltage_mv(void);

/** Read shunt current in milliamps, signed (returns 0x7FFF on error) */
int16_t ina219_read_current_ma(void);

/** Read computed power in milliwatts (returns 0xFFFF on error) */
uint16_t ina219_read_power_mw(void);

/** Check if a new conversion is ready (returns true if ready) */
bool ina219_conversion_ready(void);

#ifdef __cplusplus
}
#endif

#endif /* __INA219_H */
