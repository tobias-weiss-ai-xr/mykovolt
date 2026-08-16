# Test Fixture Firmware Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the test fixture firmware — INA219/SHT30 drivers, load bank control, and a measurement application with three modes (V_OC tracking, I/V sweep, load life test) that logs v2 FRAM entries.

**Architecture:** The test fixture is a firmware variant of the dev kit. New I2C drivers (INA219, SHT30) go in `Core/Inc` and `Core/Src` as shared infrastructure. A `testfixture/` directory holds the test fixture application (config header, main.c, CMakeLists.txt). The build produces a separate `mykovolt_testfixture.elf` target. The existing dev kit firmware remains untouched.

**Tech Stack:** C99, bare-metal STM32L011 (Cortex-M0+), ARM GCC cross-compiler, CMake build system, no HAL (direct register access)

---

## File Structure

| File | Responsibility |
|---|---|
| `firmware/Core/Inc/i2c_driver.h` | Add `i2c_read_raw()` declaration (raw read without register address) |
| `firmware/Core/Src/i2c_driver.c` | Implement `i2c_read_raw()` |
| `firmware/Core/Inc/ina219.h` | INA219 register map + public API |
| `firmware/Core/Src/ina219.c` | INA219 driver: init, read voltage/current/power |
| `firmware/Core/Inc/sht30.h` | SHT30 command defines + public API |
| `firmware/Core/Src/sht30.c` | SHT30 driver: init, read temp/humidity |
| `firmware/testfixture/testfixture_config.h` | Test fixture pin mappings, I2C addresses, FRAM v2 constants, load bank defs |
| `firmware/testfixture/testfixture_main.c` | Test fixture application: GPIO init, 3 measurement modes, v2 FRAM ring buffer, NFC command handling |
| `firmware/testfixture/CMakeLists.txt` | CMake build for `mykovolt_testfixture` target |

---

### Task 1: Add `i2c_read_raw()` to I2C driver

The SHT30 sensor uses command-based I2C (no register address for reads). After writing a 2-byte command, the master must read data bytes directly without sending a register address first. The existing `i2c_read_reg` and `i2c_read_reg16` both send a register address before reading. We need a raw read function.

**Files:**
- Modify: `firmware/Core/Inc/i2c_driver.h`
- Modify: `firmware/Core/Src/i2c_driver.c`

- [ ] **Step 1: Add declaration to i2c_driver.h**

Add after the `i2c_read_reg8` inline function (after line 76, before the "Status / Debug" section):

```c
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
```

- [ ] **Step 2: Implement in i2c_driver.c**

Add at the end of the file (after `i2c_read_reg16`, before the final blank line):

```c
/* ========================================================================
 *   Raw read (no register address)
 * ======================================================================== */

bool i2c_read_raw(uint8_t addr, uint8_t *data, uint16_t len) {
    if (i2c_busy || len == 0) return false;
    i2c_busy = true;

    if (!wait_for_flag(I2C_ISR_BUSY, false)) {
        I2C1->ICR = 0xFFFFFFFF;
        i2c_busy = false;
        return false;
    }

    /* Start + read directly (no register address phase) */
    I2C1->CR2 = (addr << 1) | I2C_CR2_START | I2C_CR2_RD_WRN;
    I2C1->CR2 |= len | I2C_CR2_AUTOEND;

    for (uint16_t i = 0; i < len; i++) {
        if (!wait_for_flag(I2C_ISR_RXNE, true)) {
            i2c_busy = false;
            return false;
        }
        data[i] = I2C1->RXDR;
    }

    if (!wait_for_flag(I2C_ISR_STOPF, true)) {
        i2c_busy = false;
        return false;
    }

    I2C1->ICR = I2C_ICR_STOPCF;
    i2c_busy = false;
    return true;
}
```

- [ ] **Step 3: Verify dev kit firmware still compiles**

Run: `cd firmware/build && cmake .. && make -j4`
Expected: PASS — `[100%] Built target mykovolt_firmware` (existing build unaffected)

- [ ] **Step 4: Commit**

```bash
git add firmware/Core/Inc/i2c_driver.h firmware/Core/Src/i2c_driver.c
git commit -m "feat: add i2c_read_raw() for command-based I2C devices"
```

---

### Task 2: INA219 driver

The INA219 is a I2C current/voltage/power sensor with a shunt resistor. It measures bus voltage (0-26V or 0-32V) and shunt voltage (±320mV). The test fixture uses it to measure pressling output voltage and current.

Shunt resistor: 0.1 Ω. Bus voltage range: 32V. ADC: 12-bit.

**Register map:**
- 0x00 Configuration (16-bit)
- 0x01 Shunt voltage (16-bit, signed, 10µV/LSB)
- 0x02 Bus voltage (16-bit, bits[15:3] = voltage in 4mV steps, bit[1] = CNVR, bit[0] = OVF)
- 0x03 Power (16-bit)
- 0x04 Current (16-bit, signed)
- 0x05 Calibration (16-bit)

**Files:**
- Create: `firmware/Core/Inc/ina219.h`
- Create: `firmware/Core/Src/ina219.c`

- [ ] **Step 1: Create ina219.h**

```c
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
```

- [ ] **Step 2: Create ina219.c**

```c
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
```

- [ ] **Step 3: Verify it compiles standalone (syntax check)**

Run: `arm-none-eabi-gcc -c -mcpu=cortex-m0plus -mthumb -Os -Wall -Wextra -Werror=implicit-function-declaration -I firmware/Core/Inc -DSTM32L011xx firmware/Core/Src/ina219.c -o /tmp/ina219.o`
Expected: PASS — no errors or warnings

- [ ] **Step 4: Commit**

```bash
git add firmware/Core/Inc/ina219.h firmware/Core/Src/ina219.c
git commit -m "feat: add INA219 current/voltage/power sensor driver"
```

---

### Task 3: SHT30 driver

The SHT30 is an I2C temperature and humidity sensor. It uses command-based addressing: the master writes a 2-byte command, waits for conversion, then reads 6 bytes (temp MSB, temp LSB, temp CRC8, humidity MSB, humidity LSB, humidity CRC8).

**Files:**
- Create: `firmware/Core/Inc/sht30.h`
- Create: `firmware/Core/Src/sht30.c`

- [ ] **Step 1: Create sht30.h**

```c
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

#ifdef __cplusplus
}
#endif

#endif /* __SHT30_H */
```

- [ ] **Step 2: Create sht30.c**

```c
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
```

- [ ] **Step 3: Verify it compiles standalone (syntax check)**

Run: `arm-none-eabi-gcc -c -mcpu=cortex-m0plus -mthumb -Os -Wall -Wextra -Werror=implicit-function-declaration -I firmware/Core/Inc -DSTM32L011xx firmware/Core/Src/sht30.c -o /tmp/sht30.o`
Expected: PASS — no errors or warnings

- [ ] **Step 4: Commit**

```bash
git add firmware/Core/Inc/sht30.h firmware/Core/Src/sht30.c
git commit -m "feat: add SHT30 temperature/humidity sensor driver"
```

---

### Task 4: Test fixture config header

This header defines the test fixture's pin mappings, I2C addresses, and FRAM v2 constants. It replaces `mykovolt.h` for the test fixture build. The test fixture removes the FDC1004 capacitance sensor and repurposes those pins for the 4 MOSFET load bank gates.

**Pin assignments (STM32L011F4Px):**

| Pin | Dev Kit | Test Fixture |
|---|---|---|
| PA0 | V_SENSE (ADC) | LOAD_R1 gate (10 kΩ) |
| PA1 | SENSOR_RDY | LOAD_R2 gate (100 Ω) |
| PA2 | USART_TX | LOAD_R3 gate (10 Ω) |
| PA3 | USART_RX | LOAD_R4 gate (1 Ω) |
| PA4 | LOAD_SW_GATE | LOAD_SW_GATE (keep) |
| PA5 | NFC_IRQ | NFC_IRQ (keep) |
| PA6 | RTC_INT | RTC_INT (keep) |
| PA7 | LED_CTRL | LED_CTRL (keep) |
| PA9 | I2C1_SCL | I2C1_SCL (keep) |
| PA10 | I2C1_SDA | I2C1_SDA (keep) |
| PB1 | VBAT_OK | VBAT_OK (keep) |

**Files:**
- Create: `firmware/testfixture/testfixture_config.h`

- [ ] **Step 1: Create testfixture_config.h**

```c
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
#define PIN_LOAD_R1          GPIO_PIN_6    /* PA0 — 10 kΩ load (trickle) */
#define PORT_LOAD_R1         GPIOA
#define PIN_LOAD_R2          GPIO_PIN_7    /* PA1 — 100 Ω load (low) */
#define PORT_LOAD_R2         GPIOA
#define PIN_LOAD_R3          GPIO_PIN_8    /* PA2 — 10 Ω load (medium) */
#define PORT_LOAD_R3         GPIOA
#define PIN_LOAD_R4          GPIO_PIN_9    /* PA3 — 1 Ω load (heavy) */
#define PORT_LOAD_R4         GPIOA

/* Power management — BQ25570 */
#define PIN_VBAT_OK          GPIO_PIN_14   /* PB1 — VBAT_OK indicator */
#define PIN_LOAD_SW_GATE     GPIO_PIN_10   /* PA4 — Q1 gate control */

/* NFC — ST25DV04K */
#define PIN_NFC_IRQ          GPIO_PIN_11   /* PA5 — NFC interrupt */

/* RTC — PCF8523 */
#define PIN_RTC_INT          GPIO_PIN_12   /* PA6 — RTC interrupt */

/* LED */
#define PIN_LED_CTRL         GPIO_PIN_13   /* PA7 — yellow LED */

/* I2C1 */
#define PIN_I2C1_SCL         GPIO_PIN_17   /* PA9 */
#define PIN_I2C1_SDA         GPIO_PIN_18   /* PA10 */

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
```

- [ ] **Step 2: Commit**

```bash
git add firmware/testfixture/testfixture_config.h
git commit -m "feat: add test fixture config header (pin map, I2C addrs, FRAM v2)"
```

---

### Task 5: Test fixture main application

This is the core application for the test fixture. It implements:
- GPIO init for 4 MOSFET load bank gates
- Three measurement modes (V_OC tracking, I/V sweep, load life test)
- v2 FRAM ring buffer (13-byte entries)
- NFC command handling (mode selection, read data)
- Sleep/wake via RTC alarm (same as dev kit)

**FRAM v2 entry format (13 bytes):**
| Offset | Field | Type |
|---|---|---|
| 0 | timestamp (sleep cycle count) | uint32 (4 bytes) |
| 4 | V_OC (mV) | uint16 (2 bytes) |
| 6 | load_current (mA, signed) | int16 (2 bytes) |
| 8 | load_resistor_index (0=none, 1-4=R1-R4) | uint8 |
| 9 | temperature (°C, signed) | int8 |
| 10 | humidity (% RH) | uint8 |
| 11 | status flags | uint8 |
| 12 | CRC (XOR of bytes 0-11) | uint8 |

**NFC command protocol (via ST25DV04K mailbox):**
- Byte 0 = command: `M` (set mode), `S` (start sweep now), `R` (read status)
- For `M`: byte 1 = mode (0/1/2), byte 2 = load mask (for load life test)
- Reply: 16-byte status packet with current mode, V_OC, I, entry count

**Files:**
- Create: `firmware/testfixture/testfixture_main.c`

- [ ] **Step 1: Create testfixture_main.c**

```c
/**
 * @file    testfixture_main.c
 * @brief   MykoVolt Test Fixture — main application
 *
 * ── System Overview ──
 *   MCU:      STM32L011F4 (Cortex-M0+, 16MHz, 16KB flash, 2KB RAM)
 *   Power:    USB (benchtop) or BQ25570 (pressling, in-soil)
 *   Storage:  MB85RC16 (2KB FRAM, I2C 0x50)
 *   Sensors:  INA219 (V/I/P, I2C 0x40), SHT30 (T/RH, I2C 0x44)
 *   RTC:      PCF8523 (I2C 0x52, alarm wake)
 *   NFC:      ST25DV04K (I2C 0x53 + RF ISO 15693)
 *   Load:     4× MOSFET-switched resistors (PA0-PA3)
 *
 * ── Measurement Modes ──
 *   V_OC_TRACKING: V_OC every 60s, all loads off
 *   IV_SWEEP:      Full I/V sweep (R1→R2→R3→R4) every 60 min
 *   LOAD_LIFE:     Fixed load, V+I every 60s until cutoff
 *
 * ── Application States ──
 *   SLEEP ──> ACTIVE ──> SLEEP  (RTC alarm wake)
 *              └──> NFC_ACCESS   (when RF field detected)
 */

#include "testfixture_config.h"
#include "i2c_driver.h"
#include "ina219.h"
#include "sht30.h"
#include "st25dv04k.h"
#include "mb85rc16.h"
#include "pcf8523.h"
#include "bq25570.h"

#include <string.h>

/* ========================================================================
 *   Local state
 * ======================================================================== */

static app_state_t g_app_state = APP_STATE_SLEEP;
static uint32_t    g_sleep_cycles = 0;
static uint8_t     g_nfc_buffer[128];

static measurement_mode_t g_mode = DEFAULT_MODE;
static uint8_t  g_load_mask = LOAD_R1_MASK;  /* Default load for load-life mode */
static uint32_t g_last_sweep_cycle = 0;       /* Cycle count of last I/V sweep */

/* Ring buffer state */
static uint16_t g_fram_write_pos = 0;
static uint16_t g_fram_entry_count = 0;

/* ========================================================================
 *   Forward declarations
 * ======================================================================== */

static void system_clock_init(void);
static void gpio_init(void);
static void enter_sleep(void);
static void do_measurement(void);
static void handle_nfc_access(void);
static void log_error(const char *msg);

static void load_bank_set(uint8_t mask);
static void load_bank_off(void);

static bool fram_ringbuffer_init(void);
static bool fram_ringbuffer_write(uint32_t timestamp, uint16_t voc_mv,
                                   int16_t load_current_ma, uint8_t load_idx,
                                   int8_t temp_c, uint8_t rh_pct,
                                   uint8_t status);
static uint8_t entry_crc(const uint8_t *data, uint8_t len);

/* ========================================================================
 *   main
 * ======================================================================== */

int main(void) {
    system_clock_init();
    gpio_init();
    i2c_init();

    bq25570_init();

    if (!ina219_init()) {
        log_error("INA219 init failed");
    }
    if (!sht30_init()) {
        log_error("SHT30 init failed");
    }
    if (!st25dv04k_init()) {
        log_error("ST25DV04K init failed");
    }
    if (!pcf8523_init()) {
        log_error("PCF8523 init failed");
    }
    if (!mb85rc16_init()) {
        log_error("MB85RC16 init failed");
    }

    fram_ringbuffer_init();

    while (1) {
        switch (g_app_state) {
        case APP_STATE_SLEEP:
            if (st25dv04k_rf_present()) {
                g_app_state = APP_STATE_NFC_ACCESS;
                break;
            }
            if (bq25570_vbat_ok()) {
                enter_sleep();
                g_sleep_cycles++;
                g_app_state = APP_STATE_ACTIVE;
            } else {
                for (volatile int i = 0; i < 500000; i++);
                g_app_state = APP_STATE_SLEEP;
            }
            break;

        case APP_STATE_ACTIVE:
            do_measurement();
            g_app_state = APP_STATE_SLEEP;
            break;

        case APP_STATE_NFC_ACCESS:
            handle_nfc_access();
            g_app_state = APP_STATE_SLEEP;
            break;

        case APP_STATE_ERROR:
            for (volatile int i = 0; i < 1000000; i++);
            g_app_state = APP_STATE_SLEEP;
            break;
        }
    }
}

/* ========================================================================
 *   System clock: HSI 16MHz
 * ======================================================================== */

static void system_clock_init(void) {
    RCC->CR |= RCC_CR_HSION;
    while (!(RCC->CR & RCC_CR_HSIRDY));

    RCC->CFGR = (RCC->CFGR & ~RCC_CFGR_SW) | RCC_CFGR_SW_HSI;
    while ((RCC->CFGR & RCC_CFGR_SWS) != RCC_CFGR_SWS_HSI);

    RCC->CFGR &= ~(RCC_CFGR_HPRE | RCC_CFGR_PPRE1 | RCC_CFGR_PPRE2);
    RCC->CSR |= RCC_CSR_LSEON;
}

/* ========================================================================
 *   GPIO
 * ======================================================================== */

static void gpio_init(void) {
    RCC->IOPENR |= RCC_IOPENR_GPIOAEN | RCC_IOPENR_GPIOBEN | RCC_IOPENR_GPIOCEN;

    /* LED2 (PA7) — push-pull output */
    GPIOA->MODER &= ~GPIO_MODER_MODE7_Msk;
    GPIOA->MODER |= GPIO_MODER_MODE7_0;
    GPIOA->OTYPER &= ~GPIO_OTYPER_OT_7;
    GPIOA->PUPDR &= ~GPIO_PUPDR_PUPD7_Msk;

    /* LOAD_SW_GATE (PA4) — push-pull output, initially on */
    GPIOA->MODER &= ~GPIO_MODER_MODE4_Msk;
    GPIOA->MODER |= GPIO_MODER_MODE4_0;
    GPIOA->OTYPER &= ~GPIO_OTYPER_OT_4;
    GPIOA->PUPDR &= ~GPIO_PUPDR_PUPD4_Msk;
    GPIOA->BSRR = GPIO_BSRR_BS_4;

    /* Load bank MOSFET gates: PA0 (R1), PA1 (R2), PA2 (R3), PA3 (R4) */
    /* All push-pull outputs, initially OFF (loads disconnected) */
    for (int pin = 0; pin <= 3; pin++) {
        GPIOA->MODER &= ~(3U << (pin * 2));
        GPIOA->MODER |= (1U << (pin * 2));    /* Output mode */
        GPIOA->OTYPER &= ~(1U << pin);         /* Push-pull */
        GPIOA->PUPDR &= ~(3U << (pin * 2));    /* No pull */
        GPIOA->BSRR = (1U << (pin + 16));      /* Reset (OFF) */
    }

    /* NFC IRQ (PA5) — input with pull-up */
    GPIOA->MODER &= ~GPIO_MODER_MODE5_Msk;
    GPIOA->PUPDR &= ~GPIO_PUPDR_PUPD5_Msk;
    GPIOA->PUPDR |= GPIO_PUPDR_PUPD5_0;

    /* VBAT_OK (PB1) — input */
    GPIOB->MODER &= ~GPIO_MODER_MODE1_Msk;

    /* RTC_INT (PA6) — input with falling-edge IRQ */
    GPIOA->MODER &= ~GPIO_MODER_MODE6_Msk;
    GPIOA->PUPDR &= ~GPIO_PUPDR_PUPD6_Msk;
    GPIOA->PUPDR |= GPIO_PUPDR_PUPD6_0;

    SYSCFG->EXTICR[1] &= ~SYSCFG_EXTICR_EXTI6;
    SYSCFG->EXTICR[1] |= SYSCFG_EXTICR_EXTI6_PA;
    EXTI->IMR |= EXTI_IMR_IM6;
    EXTI->FTSR |= EXTI_FTSR_TR6;

    NVIC_EnableIRQ(EXTI4_15_IRQn);
}

/* ========================================================================
 *   Load bank control
 * ======================================================================== */

static void load_bank_set(uint8_t mask) {
    /* PA0=R1, PA1=R2, PA2=R3, PA3=R4 */
    if (mask & LOAD_R1_MASK) GPIOA->BSRR = GPIO_BSRR_BS_0;
    else                     GPIOA->BSRR = GPIO_BSRR_BR_0;
    if (mask & LOAD_R2_MASK) GPIOA->BSRR = GPIO_BSRR_BS_1;
    else                     GPIOA->BSRR = GPIO_BSRR_BR_1;
    if (mask & LOAD_R3_MASK) GPIOA->BSRR = GPIO_BSRR_BS_2;
    else                     GPIOA->BSRR = GPIO_BSRR_BR_2;
    if (mask & LOAD_R4_MASK) GPIOA->BSRR = GPIO_BSRR_BS_3;
    else                     GPIOA->BSRR = GPIO_BSRR_BR_3;
}

static void load_bank_off(void) {
    GPIOA->BSRR = GPIO_BSRR_BR_0 | GPIO_BSRR_BR_1 | GPIO_BSRR_BR_2 | GPIO_BSRR_BR_3;
}

/* ========================================================================
 *   Sleep mode (STOP with RTC alarm wake)
 * ======================================================================== */

static void enter_sleep(void) {
    GPIOA->BSRR = GPIO_BSRR_BR_7;

    pcf8523_clear_alarm();

    pcf8523_datetime_t dt;
    if (pcf8523_read_datetime(&dt)) {
        pcf8523_set_minute_alarm((dt.minutes + 1) % 60);
    }

    PWR->CR |= PWR_CR_LPSDSR;
    PWR->CR |= PWR_CR_ULP;
    SCB->SCR |= SCB_SCR_SLEEPDEEP_Msk;
    __WFI();

    GPIOA->BSRR = GPIO_BSRR_BS_7;
}

/* ========================================================================
 *   Measurement cycle
 * ======================================================================== */

static void do_measurement(void) {
    int8_t  temp_c = 0;
    uint8_t rh_pct = 0;
    sht30_read(&temp_c, &rh_pct);

    uint8_t status = 0;
    if (bq25570_vbat_ok()) status |= 0x01;
    if (st25dv04k_rf_present()) status |= 0x02;

    switch (g_mode) {
    case MODE_VOC_TRACKING: {
        /* V_OC measurement: all loads off, read voltage */
        load_bank_off();
        uint16_t voc = ina219_read_voltage_mv();
        fram_ringbuffer_write(g_sleep_cycles, voc, 0, 0,
                              temp_c, rh_pct, status);
        break;
    }

    case MODE_IV_SWEEP: {
        /* Full I/V sweep every MEASURE_INTERVAL_SWEEP / RTC_interval cycles
         * Otherwise just V_OC tracking */
        uint32_t sweep_period = MEASURE_INTERVAL_SWEEP / 60;  /* cycles between sweeps (60s/cycle) */
        if (sweep_period == 0) sweep_period = 1;

        if ((g_sleep_cycles - g_last_sweep_cycle) >= sweep_period) {
            g_last_sweep_cycle = g_sleep_cycles;

            /* Sweep each load: R1, R2, R3, R4 */
            const uint8_t loads[] = {LOAD_R1_MASK, LOAD_R2_MASK,
                                      LOAD_R3_MASK, LOAD_R4_MASK};
            for (int i = 0; i < 4; i++) {
                load_bank_set(loads[i]);
                /* Dwell SWEEP_DWELL_MS (approximate busy-wait) */
                for (volatile int j = 0; j < SWEEP_DWELL_MS * 200; j++);
                uint16_t v = ina219_read_voltage_mv();
                int16_t  i_ma = ina219_read_current_ma();
                fram_ringbuffer_write(g_sleep_cycles, v, i_ma,
                                      (uint8_t)(i + 1),
                                      temp_c, rh_pct, status);
            }
            load_bank_off();
        } else {
            /* Between sweeps: V_OC tracking */
            load_bank_off();
            uint16_t voc = ina219_read_voltage_mv();
            fram_ringbuffer_write(g_sleep_cycles, voc, 0, 0,
                                  temp_c, rh_pct, status);
        }
        break;
    }

    case MODE_LOAD_LIFE: {
        /* Continuous fixed load, measure V+I every cycle */
        load_bank_set(g_load_mask);
        uint16_t v = ina219_read_voltage_mv();
        int16_t  i_ma = ina219_read_current_ma();

        /* Determine load index from mask */
        uint8_t load_idx = 0;
        if (g_load_mask == LOAD_R1_MASK) load_idx = 1;
        else if (g_load_mask == LOAD_R2_MASK) load_idx = 2;
        else if (g_load_mask == LOAD_R3_MASK) load_idx = 3;
        else if (g_load_mask == LOAD_R4_MASK) load_idx = 4;

        fram_ringbuffer_write(g_sleep_cycles, v, i_ma, load_idx,
                              temp_c, rh_pct, status);
        break;
    }
    }
}

/* ========================================================================
 *   NFC access
 * ======================================================================== */

static void handle_nfc_access(void) {
    uint16_t msg_len = st25dv04k_mailbox_read_len();
    if (msg_len > 0 && msg_len <= sizeof(g_nfc_buffer)) {
        st25dv04k_mailbox_read(g_nfc_buffer, &msg_len);

        uint8_t cmd = g_nfc_buffer[0];
        uint8_t reply[16];
        memset(reply, 0, sizeof(reply));

        switch (cmd) {
        case 'M': /* Set mode */
            if (msg_len >= 2) {
                g_mode = (measurement_mode_t)g_nfc_buffer[1];
                if (msg_len >= 3) {
                    g_load_mask = g_nfc_buffer[2];
                }
            }
            reply[0] = 'M';
            reply[1] = (uint8_t)g_mode;
            reply[2] = g_load_mask;
            st25dv04k_mailbox_write(reply, 3);
            break;

        case 'S': /* Start sweep now */
            g_last_sweep_cycle = 0;  /* Force sweep on next active cycle */
            reply[0] = 'S';
            reply[1] = 0;  /* OK */
            st25dv04k_mailbox_write(reply, 2);
            break;

        case 'R': /* Read status */
            reply[0] = 'R';
            reply[1] = (uint8_t)g_mode;
            reply[2] = g_load_mask;
            /* Current V_OC and current */
            load_bank_off();
            uint16_t voc = ina219_read_voltage_mv();
            reply[3] = (uint8_t)(voc >> 8);
            reply[4] = (uint8_t)(voc);
            int16_t cur = ina219_read_current_ma();
            reply[5] = (uint8_t)((uint16_t)cur >> 8);
            reply[6] = (uint8_t)((uint16_t)cur);
            /* Entry count */
            reply[7] = (uint8_t)(g_fram_entry_count >> 8);
            reply[8] = (uint8_t)(g_fram_entry_count);
            st25dv04k_mailbox_write(reply, 9);
            break;

        default:
            reply[0] = '?';
            st25dv04k_mailbox_write(reply, 1);
            break;
        }
    }

    volatile uint32_t timeout = 1000000;
    while (st25dv04k_rf_present() && timeout--) {}
}

/* ========================================================================
 *   FRAM ring buffer (v2 — 13-byte entries)
 * ======================================================================== */

static bool fram_ringbuffer_init(void) {
    uint8_t magic_hi = mb85rc16_read_byte(0x00);
    uint8_t magic_lo = mb85rc16_read_byte(0x01);

    if (magic_hi == 0xFF && magic_lo == 0xFF) {
        /* First boot — initialise header */
        uint8_t hdr[5];
        hdr[0] = (FRAM_MAGIC >> 8) & 0xFF;
        hdr[1] = FRAM_MAGIC & 0xFF;
        hdr[2] = FRAM_VERSION;
        hdr[3] = 0;  /* Write pos high */
        hdr[4] = 0;  /* Write pos low */
        if (!mb85rc16_write(0x00, hdr, 5)) {
            return false;
        }
        g_fram_write_pos = 0;
        g_fram_entry_count = 0;
        return true;
    }

    /* Existing data — resume write pointer */
    uint8_t pos_buf[2];
    if (mb85rc16_read(0x03, pos_buf, 2) == 2) {
        g_fram_write_pos = ((uint16_t)pos_buf[0] << 8) | pos_buf[1];
    } else {
        g_fram_write_pos = 0;
    }
    g_fram_entry_count = g_fram_write_pos / FRAM_ENTRY_SIZE;
    return true;
}

static bool fram_ringbuffer_write(uint32_t timestamp, uint16_t voc_mv,
                                   int16_t load_current_ma, uint8_t load_idx,
                                   int8_t temp_c, uint8_t rh_pct,
                                   uint8_t status) {
    uint8_t entry[FRAM_ENTRY_SIZE];
    uint16_t addr;

    entry[0] = (uint8_t)(timestamp >> 24);
    entry[1] = (uint8_t)(timestamp >> 16);
    entry[2] = (uint8_t)(timestamp >> 8);
    entry[3] = (uint8_t)(timestamp);
    entry[4] = (uint8_t)(voc_mv >> 8);
    entry[5] = (uint8_t)(voc_mv);
    entry[6] = (uint8_t)((uint16_t)load_current_ma >> 8);
    entry[7] = (uint8_t)((uint16_t)load_current_ma);
    entry[8] = load_idx;
    entry[9] = (uint8_t)temp_c;
    entry[10] = rh_pct;
    entry[11] = status;
    entry[12] = entry_crc(entry, FRAM_ENTRY_SIZE - 1);

    addr = FRAM_DATA_START + g_fram_write_pos;

    if (g_fram_entry_count >= FRAM_MAX_ENTRIES) {
        g_fram_write_pos = 0;
        addr = FRAM_DATA_START;
    }

    if (!mb85rc16_write(addr, entry, FRAM_ENTRY_SIZE)) {
        return false;
    }

    g_fram_write_pos += FRAM_ENTRY_SIZE;
    g_fram_entry_count++;

    uint8_t pos_buf[2];
    pos_buf[0] = (uint8_t)(g_fram_write_pos >> 8);
    pos_buf[1] = (uint8_t)(g_fram_write_pos);
    return mb85rc16_write(0x03, pos_buf, 2);
}

static uint8_t entry_crc(const uint8_t *data, uint8_t len) {
    uint8_t crc = 0;
    for (uint8_t i = 0; i < len; i++) {
        crc ^= data[i];
    }
    return crc;
}

/* ========================================================================
 *   Error logging (LED blink pattern)
 * ======================================================================== */

static void log_error(const char *msg) {
    (void)msg;
    for (int i = 0; i < 3; i++) {
        GPIOA->BSRR = GPIO_BSRR_BS_7;
        for (volatile int j = 0; j < 200000; j++);
        GPIOA->BSRR = GPIO_BSRR_BR_7;
        for (volatile int j = 0; j < 200000; j++);
    }
}

/* ========================================================================
 *   EXTI4_15_IRQHandler (RTC alarm on PA6 / EXTI6)
 * ======================================================================== */

void EXTI4_15_IRQHandler(void) {
    if (EXTI->PR & EXTI_PR_PR6) {
        EXTI->PR = EXTI_PR_PR6;
    }
}
```

- [ ] **Step 2: Commit**

```bash
git add firmware/testfixture/testfixture_main.c
git commit -m "feat: add test fixture main application (3 measurement modes, v2 FRAM)"
```

---

### Task 6: Test fixture CMakeLists.txt

Create a separate CMake build target for the test fixture firmware. It shares the same MCU, toolchain, linker script, and startup file as the dev kit, but compiles different source files (testfixture_main.c instead of main.c, adds ina219.c and sht30.c, removes fdc1004.c).

**Files:**
- Create: `firmware/testfixture/CMakeLists.txt`

- [ ] **Step 1: Create testfixture CMakeLists.txt**

```cmake
cmake_minimum_required(VERSION 3.14)

project(mykovolt_testfixture
    VERSION 0.1
    LANGUAGES C ASM
)

# ── Target ──
set(TARGET mykovolt_testfixture)

# ── MCU settings (same as dev kit) ──
set(MCU_FAMILY    STM32L011xx)
set(MCU_CORE      cortex-m0plus)
set(FLASH_SIZE    16K)
set(RAM_SIZE      2K)

# ── Sources ──
# Test fixture application + shared drivers (no fdc1004, no dev-kit main.c)
set(CORE_SRC
    ${CMAKE_CURRENT_SOURCE_DIR}/testfixture_main.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../Core/Src/i2c_driver.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../Core/Src/ina219.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../Core/Src/sht30.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../Core/Src/st25dv04k.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../Core/Src/mb85rc16.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../Core/Src/pcf8523.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../Core/Src/bq25570.c
)

set(STARTUP_SRC
    ${CMAKE_CURRENT_SOURCE_DIR}/../startup/startup_stm32l011xx.s
    ${CMAKE_CURRENT_SOURCE_DIR}/../Drivers/CMSIS/Device/ST/STM32L0xx/system_stm32l0xx.c
)

# ── Includes ──
set(CORE_INC
    ${CMAKE_CURRENT_SOURCE_DIR}           # testfixture_config.h
    ${CMAKE_CURRENT_SOURCE_DIR}/../Core/Inc  # shared driver headers
)

set(CMSIS_INC
    ${CMAKE_CURRENT_SOURCE_DIR}/../Drivers/CMSIS/Include
    ${CMAKE_CURRENT_SOURCE_DIR}/../Drivers/CMSIS/Device/ST/STM32L0xx/Include
)

# ── Compile options ──
add_compile_options(
    -mcpu=${MCU_CORE}
    -mthumb
    -mfloat-abi=soft
    -ffunction-sections
    -fdata-sections
    -Wall
    -Wextra
    -Werror=implicit-function-declaration
    -Os
    -g
)

add_compile_definitions(
    ${MCU_FAMILY}
    HSE_VALUE=16000000
)

# ── Link options ──
add_link_options(
    -mcpu=${MCU_CORE}
    -mthumb
    -mfloat-abi=soft
    -specs=nano.specs
    -specs=nosys.specs
    -Wl,--gc-sections
    -Wl,-Map=${TARGET}.map
    -T${CMAKE_CURRENT_SOURCE_DIR}/../startup/STM32L011F4Px.ld
)

# ── Build the executable ──
add_executable(${TARGET}
    ${CORE_SRC}
    ${STARTUP_SRC}
)

target_include_directories(${TARGET} PRIVATE
    ${CORE_INC}
    ${CMSIS_INC}
)

# ── Post-build: generate hex ──
add_custom_command(TARGET ${TARGET} POST_BUILD
    COMMAND ${CMAKE_OBJCOPY} -O ihex ${TARGET} ${TARGET}.hex
    COMMAND ${CMAKE_SIZE} ${TARGET}
    COMMENT "Generating ${TARGET}.hex"
)

# ── Toolchain file path ──
set(CMAKE_TOOLCHAIN_FILE ${CMAKE_CURRENT_SOURCE_DIR}/../cmake/arm-gcc-toolchain.cmake CACHE FILEPATH "ARM GCC toolchain")
```

- [ ] **Step 2: Commit**

```bash
git add firmware/testfixture/CMakeLists.txt
git commit -m "feat: add test fixture CMakeLists.txt build target"
```

---

### Task 7: Verify compilation and check flash/RAM usage

Build the test fixture firmware, verify it compiles cleanly with no warnings, and check that flash usage fits within the 16KB limit.

**Files:**
- No new files — verification only

- [ ] **Step 1: Create build directory and configure**

Run: `mkdir -p firmware/testfixture/build && cd firmware/testfixture/build && cmake ..`
Expected: CMake configures successfully

- [ ] **Step 2: Build**

Run: `make -j4`
Expected: `[100%] Built target mykovolt_testfixture` — no errors, no warnings

- [ ] **Step 3: Check binary size**

Run: `arm-none-eabi-size firmware/testfixture/build/mykovolt_testfixture.elf`
Expected: text + data < 16KB (16384 bytes), bss < 2KB (2048 bytes)

- [ ] **Step 4: Verify hex file exists**

Run: `ls -la firmware/testfixture/build/mykovolt_testfixture.hex`
Expected: File exists, non-zero size

- [ ] **Step 5: Commit build results note (no binary artifacts)**

If any source fixes were needed during build, commit them:
```bash
git add -A firmware/testfixture/ firmware/Core/
git commit -m "fix: resolve compilation issues in test fixture firmware"
```

If no fixes were needed, skip this step.
