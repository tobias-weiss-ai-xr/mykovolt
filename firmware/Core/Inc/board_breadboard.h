/**
 * @file    board_breadboard.h
 * @brief   Pin mappings for MykoVolt breadboard prototype using Nucleo-L011K4
 *
 * Nucleo-L011K4 pinout: https://www.st.com/resource/en/user_manual/dm00231744.pdf
 *
 * To use: #define BOARD_BREADBOARD 1 in your build or add -DBOARD_BREADBOARD=1
 */

#ifndef __BOARD_BREADBOARD_H
#define __BOARD_BREADBOARD_H

#ifdef __cplusplus
extern "C" {
#endif

#include "mykovolt.h"

/* ========================================================================
 *   Nucleo-L011K4 to DevKit Pin Mapping
 * ========================================================================
 *
 * Nucleo connector (CN9 / morpho):
 *   CN9-7  = PA9  = I2C1_SCL  → SCL bus
 *   CN9-15 = PA10 = I2C1_SDA  → SDA bus
 *   CN9-24 = PA2  = USART_TX  → virtual COM (via ST-Link)
 *   CN9-23 = PA3  = USART_RX  ← virtual COM
 *   CN9-29 = PA1  = SENSOR_RDY (FDC1004)
 *   CN10-20 = PA0  = V_SENSE (ADC)
 *   CN10-25 = PA4  = LOAD_SW_GATE
 *   CN10-12 = PA5  = NFC_IRQ
 *   CN10-11 = PA6  = RTC_INT
 *   CN10-10 = PA7  = LED_CTRL (yellow LED)
 *   CN10-28 = PB1  = VBAT_OK
 *   CN10-24 = PB9  = free GPIO
 */

/* ── Redefine pins for Nucleo form factor ── */

/* On Nucleo, the yellow LED is on PA5 (LD2), not PA7.
   We use PB3 (CN10-31) for LED_CTRL instead to keep PA5 free for NFC_IRQ. */
#undef  PIN_LED_CTRL
#define PIN_LED_CTRL            GPIO_PIN_3     /* PB3  — Nucleo D3 / CN10-31 */

/* Nucleo has a built-in green LED on PB3 (LD3), which we repurpose as power LED.
   The external LED1 on the breadboard can connect to D9 (PA7). */

/* ========================================================================
 *   Nucleo-Specific Peripheral Overrides
 * ======================================================================== */

/* The Nucleo-L011K4 uses an external 32.768kHz crystal for the ST-Link RTC,
   but NOT for the target MCU. The target MCU runs on HSI (16MHz) only.
   Comment this out if you add an external crystal to the breadboard. */
#define NUCLEO_NO_LSE           1

/* ST-Link virtual COM port is on PA2 (TX) / PA3 (RX) via USART2.
   The DevKit schematic routes USART_TX/RX to J1 header pins 8/6 (PA2/PA3).
   On Nucleo, these are already connected to the ST-Link. */
#define USE_STLINK_VCOM         1

/* ========================================================================
 *   I2C Pull-up Resistors
 * ======================================================================== */

/* Nucleo-L011K4 has built-in 4.7kΩ pull-ups on D14/D15.
   If you also add external 2.2kΩ resistors (R1, R2), the parallel
   equivalent is ~1.5kΩ which is fine for standard mode (100kHz). */

/* ========================================================================
 *   Breadboard-Specific Macros
 * ======================================================================== */

/* Macro to check if we're on breadboard vs PCB */
#if defined(BOARD_BREADBOARD) && BOARD_BREADBOARD
  #define IS_BREADBOARD()       1
#else
  #define IS_BREADBOARD()       0
#endif

/** ADC reference voltage on Nucleo (from ST-Link VREF) */
#define ADC_VREF_MV             3300

/** Voltage divider for V_SENSE: same as PCB (R9=100k, R10=220k) */
#define V_SENSE_DIVIDER         ((100.0f + 220.0f) / 100.0f)

#ifdef __cplusplus
}
#endif

#endif /* __BOARD_BREADBOARD_H */
