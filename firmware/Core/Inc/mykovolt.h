/**
 * @file    mykovolt.h
 * @brief   MykoVolt DevKit — board definitions, pin mappings, I2C addresses
 * 
 * MCU: STM32L011F4Px (TSSOP-20)
 * Toolchain: ARM GCC / STM32CubeMX
 */

#ifndef __MYKOVOLT_H
#define __MYKOVOLT_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>

/* ========================================================================
 *   Pin Mappings (STM32L011F4Px TSSOP-20)
 * ======================================================================== */

/* Power management — BQ25570 */
#define PIN_VBAT_OK          GPIO_PIN_14   /* PB1  — VBAT_OK indicator */
#define PIN_LOAD_SW_GATE     GPIO_PIN_10   /* PA4  — Q1 gate control */

/* NFC — ST25DV04K */
#define PIN_NFC_IRQ          GPIO_PIN_11   /* PA5  — NFC interrupt */

/* RTC — PCF8523 */
#define PIN_RTC_INT          GPIO_PIN_12   /* PA6  — RTC interrupt */

/* Capacitance sensor — FDC1004 */
#define PIN_SENSOR_RDY       GPIO_PIN_7    /* PA1  — sensor ready */

/* Debug / UART */
#define PIN_USART_TX         GPIO_PIN_8    /* PA2  */
#define PIN_USART_RX         GPIO_PIN_9    /* PA3  */

/* LEDs */
#define PIN_LED_CTRL         GPIO_PIN_13   /* PA7  — yellow LED (LED2) */

/* ADC */
#define PIN_V_SENSE          GPIO_PIN_6    /* PA0  — battery voltage */

/* I2C1 */
#define PIN_I2C1_SCL         GPIO_PIN_17   /* PA9  */
#define PIN_I2C1_SDA         GPIO_PIN_18   /* PA10 */

/* ========================================================================
 *   I2C Address Map
 * ======================================================================== */

#define I2C_ADDR_FRAM        0x50  /* MB85RC16 */
#define I2C_ADDR_FDC1004     0x51  /* Capacitance sensor */
#define I2C_ADDR_PCF8523     0x52  /* RTC */
#define I2C_ADDR_ST25DV04K   0x53  /* NFC tag */

/* ========================================================================
 *   Power Management
 * ======================================================================== */

/** BQ25570 VBAT_OK threshold (typical, configured via resistor divider) */
#define VBAT_OK_THRESHOLD_MV 3100

/** V_SENSE divider ratio (R9=100k, R10=220k) */
#define V_SENSE_DIVIDER_RATIO ((100.0f + 220.0f) / 100.0f)

/* ========================================================================
 *   Sensor Electrodes (FDC1004)
 * ======================================================================== */

#define FDC1004_CIN1         0  /* Soil moisture channel */
#define FDC1004_CIN2         1  /* Reference / temperature comp */
#define FDC1004_CIN3         2  /* Spare */
#define FDC1004_CIN4         3  /* Shield driver (not used) */

/* ========================================================================
 *   System Clock
 * ======================================================================== */

#define LSE_FREQ_HZ          32768
#define HSI_FREQ_HZ          16000000
#define SYSCLK_FREQ_HZ       16000000

/* ========================================================================
 *   Application States
 * ======================================================================== */

typedef enum {
    APP_STATE_SLEEP,        /* Deep sleep, everything off */
    APP_STATE_ACTIVE,       /* Measuring, I2C active */
    APP_STATE_NFC_ACCESS,   /* NFC tag being read by external reader */
    APP_STATE_ERROR         /* Error condition */
} app_state_t;

#ifdef __cplusplus
}
#endif

#endif /* __MYKOVOLT_H */
