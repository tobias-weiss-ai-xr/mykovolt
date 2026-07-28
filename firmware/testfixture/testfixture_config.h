/**
 * @file    testfixture_config.h
 * @brief   MykoVolt Test Fixture — board definitions, pin mappings, I2C addresses
 *
 * MCU: STM32L011F4Px (UFQFPN-20)
 * Purpose: Characterize pressling (fungal MFC) power output
 *
 * This header replaces mykovolt.h for the test fixture build.
 * It defines different pin mappings (load bank MOSFETs instead of
 * FDC1004/USART) and additional I2C addresses (INA219, SHT30).
 */

#ifndef __TESTFIXTURE_CONFIG_H
#define __TESTFIXTURE_CONFIG_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>
#include "stm32l011xx.h"

/* ========================================================================
 *   Pin Mappings (STM32L011F4Px TSSOP-20)
 * ======================================================================== */

/* Load bank MOSFET gates (repurposed from dev kit) */
#define PIN_LOAD_R1          GPIO_PIN_0    /* PA0 — 10 kΩ load (trickle) */
#define PORT_LOAD_R1         GPIOA
#define PIN_LOAD_R2          GPIO_PIN_1    /* PA1 — 100 Ω load (low) */
#define PORT_LOAD_R2         GPIOA
#define PIN_LOAD_R3          GPIO_PIN_2    /* PA2 — 10 Ω load (medium) */
#define PORT_LOAD_R3         GPIOA
#define PIN_LOAD_R4          GPIO_PIN_3    /* PA3 — 1 Ω load (heavy) */
#define PORT_LOAD_R4         GPIOA

/* Power management — BQ25570 */
#define PIN_VBAT_OK          GPIO_PIN_1    /* PB1 — VBAT_OK indicator */
#define PORT_VBAT_OK         GPIOB
#define PIN_LOAD_SW_GATE     GPIO_PIN_4    /* PA4 — Q1 gate control */

/* NFC — ST25DV04K */
#define PIN_NFC_IRQ          GPIO_PIN_5    /* PA5 — NFC interrupt */

/* RTC — PCF8523 */
#define PIN_RTC_INT          GPIO_PIN_6    /* PA6 — RTC interrupt */

/* LED */
#define PIN_LED_CTRL         GPIO_PIN_7    /* PA7 — yellow LED */

/* I2C1 */
#define PIN_I2C1_SCL         GPIO_PIN_9    /* PA9 */
#define PIN_I2C1_SDA         GPIO_PIN_10   /* PA10 */

/* ========================================================================
 *   I2C Address Map
 * ======================================================================== */

#define I2C_ADDR_INA219      0x40  /* Current/voltage/power sensor */
#define I2C_ADDR_SHT30       0x44  /* Temperature + humidity */
#define I2C_ADDR_FRAM        0x50  /* MB85RC16 */
#define I2C_ADDR_PCF8523     0x52  /* RTC */
#define I2C_ADDR_ST25DV04K   0x53  /* NFC tag */

/* ========================================================================
 *   Load Bank
 * ======================================================================== */

#define LOAD_R1_MASK         0x01  /* 10 kΩ — trickle (40 µA at 0.4V) */
#define LOAD_R2_MASK         0x02  /* 100 Ω — low (4 mA at 0.4V) */
#define LOAD_R3_MASK         0x04  /* 10 Ω — medium (40 mA at 0.4V) */
#define LOAD_R4_MASK         0x08  /* 1 Ω — heavy (400 mA at 0.4V) */

/* ========================================================================
 *   FRAM Ring Buffer (v2 — Test Fixture Format)
 * ======================================================================== */

#define FRAM_MAGIC           0x4D56  /* "MV" — same as dev kit */
#define FRAM_VERSION         0x02    /* v2 = test fixture */
#define FRAM_HEADER_SIZE     256
#define FRAM_ENTRY_SIZE      13      /* v2 entry: 12 data + 1 CRC */
#define FRAM_DATA_START      0x100
#define FRAM_MAX_ENTRIES     ((2048 - FRAM_HEADER_SIZE) / FRAM_ENTRY_SIZE)  /* 137 */

/* ========================================================================
 *   Measurement Modes
 * ======================================================================== */

typedef enum {
    MODE_VOC_TRACKING = 0,  /* V_OC every 60s, loads off */
    MODE_IV_SWEEP      = 1,  /* Full I/V sweep every 60 min */
    MODE_LOAD_LIFE     = 2   /* Continuous fixed load, V+I every 60s */
} measurement_mode_t;

/* Default measurement interval (seconds) */
#define MEASURE_INTERVAL_VOC     60    /* V_OC tracking interval */
#define MEASURE_INTERVAL_SWEEP   3600  /* I/V sweep interval */
#define MEASURE_INTERVAL_LIFE    60    /* Load life test interval */

/* I/V sweep: dwell time per load step (ms) */
#define SWEEP_DWELL_MS           5000  /* 5 seconds per load */

/* Default mode for NFC-configured mode */
#define DEFAULT_MODE             MODE_VOC_TRACKING

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

#endif /* __TESTFIXTURE_CONFIG_H */
