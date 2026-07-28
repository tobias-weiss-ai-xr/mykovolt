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
