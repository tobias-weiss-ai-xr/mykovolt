/**
 * @file    bq25570.h
 * @brief   BQ25570 power management driver (GPIO-based)
 *
 * The BQ25570 is a boost charger + LDO for energy harvesting.
 * Communication is via GPIO pins only (no I2C/SPI):
 *   - VBAT_OK (PB1): high when battery voltage is above threshold
 *   - LOAD_SW (PA4): gate control for load switch
 */

#ifndef __BQ25570_H
#define __BQ25570_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>

/* ── Public API ── */

/** Initialise power management GPIO */
void bq25570_init(void);

/** Check if VBAT_OK is asserted (true = battery voltage > threshold) */
bool bq25570_vbat_ok(void);

/** Enable/disable the load switch (VOUT to system) */
void bq25570_load_enable(void);
void bq25570_load_disable(void);

/** Read battery voltage via V_SENSE ADC (PA0), returns mV */
uint16_t bq25570_read_voltage_mv(void);

#ifdef __cplusplus
}
#endif

#endif /* __BQ25570_H */