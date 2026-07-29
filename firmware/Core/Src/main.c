/**
 * @file    main.c
 * @brief   MykoVolt DevKit — main application
 *
 * ── System Overview ──
 *   MCU:      STM32L011F4 (Cortex-M0+, 16MHz, 16KB flash, 2KB RAM)
 *   Power:    BQ25570 (boost charger + LDO from pressling MFC)
 *   Storage:  MB85RC16 (16Kbit FRAM, I2C 0x50, 2KB)
 *   Sensor:   FDC1004 (4ch capacitance, I2C 0x51)
 *   RTC:      PCF8523 (I2C 0x52, alarm every 15 min)
 *   NFC:      ST25DV04K (I2C 0x53 + RF ISO 15693)
 *
 * ── Application States ──
 *   SLEEP ──> ACTIVE ──> SLEEP  (RTC alarm wakes every 15 min)
 *              └──> NFC_ACCESS   (when RF field detected)
 */

#include "mykovolt.h"
#include "i2c_driver.h"
#include "fdc1004.h"
#include "st25dv04k.h"
#include "mb85rc16.h"
#include "pcf8523.h"
#include "bq25570.h"

#include <string.h>

/* ========================================================================
 *   FRAM Ring Buffer Layout (MB85RC16 = 2KB)
 * ========================================================================
 *
 *   Address   | Content              | Size
 *   ----------+----------------------+-------
 *   0x000     | Magic (0x4D56 = "MV")| 2
 *   0x002     | Version              | 1
 *   0x003     | Write pointer        | 2  (byte offset from 0x100)
 *   0x005     | Reserved             | 251
 *   0x100     | Entry 0              | 12
 *   0x10C     | Entry 1              | 12
 *   ...       | ...                  | ...
 *   0x7FF     | Last entry byte      | -
 *
 *   Entry format (12 bytes):
 *     [0] timestamp  uint32  RTC counter or Unix time
 *     [4] cap_raw    uint16  FDC1004 raw value
 *     [6] v_batt     uint16  Battery voltage in mV
 *     [8] v_sense    uint16  Sensor voltage in mV
 *     [10] status    uint8   Flags (bit 0: VBAT_OK, bit 1: NFC present)
 *     [11] crc       uint8   XOR of bytes 0-10
 *
 *   Max entries: (2048 - 256) / 12 = 149
 */

#define FRAM_MAGIC          0x4D56  /* "MV" */
#define FRAM_VERSION        0x01
#define FRAM_HEADER_SIZE    256
#define FRAM_ENTRY_SIZE     12
#define FRAM_DATA_START     0x100
#define FRAM_MAX_ENTRIES    ((2048 - FRAM_HEADER_SIZE) / FRAM_ENTRY_SIZE)
#define FRAM_MEASURE_INTERVAL 10  /* Every 10th cycle = ~15 min at 90s cycle */

/* ========================================================================
 *   Local state
 * ======================================================================== */

static app_state_t g_app_state = APP_STATE_SLEEP;
static uint32_t    g_sleep_cycles = 0;
static int32_t     g_last_moisture_raw = 0;
static float       g_last_moisture_pf = 0.0f;
static uint8_t     g_nfc_buffer[128];

/* Ring buffer state */
static uint16_t    g_fram_write_pos = 0;   /* Byte offset from 0x100 */
static uint16_t    g_fram_entry_count = 0;

/* ========================================================================
 *   Forward declarations
 * ======================================================================== */

static void system_clock_init(void);
static void gpio_init(void);
static void enter_sleep(void);
static void do_measurement(void);
static void handle_nfc_access(void);
static void log_error(const char *msg);

static bool fram_ringbuffer_init(void);
static bool fram_ringbuffer_write(uint32_t timestamp, uint16_t cap_raw,
                                   uint16_t v_batt, uint16_t v_sense,
                                   uint8_t status);
static uint8_t entry_crc(const uint8_t *data);

/* ========================================================================
 *   main
 * ======================================================================== */

int main(void) {
    system_clock_init();
    gpio_init();
    i2c_init();

    bq25570_init();

    if (!fdc1004_init()) {
        log_error("FDC1004 init failed");
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

    (void)fdc1004_read_device_id();
    (void)st25dv04k_read_ic_ref();

    /* Init FRAM ring buffer (preserves existing data on reset) */
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
                /* VBAT too low — stay awake, blink, retry */
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

    /* NFC IRQ (PA5) — input with pull-up */
    GPIOA->MODER &= ~GPIO_MODER_MODE5_Msk;
    GPIOA->PUPDR &= ~GPIO_PUPDR_PUPD5_Msk;
    GPIOA->PUPDR |= GPIO_PUPDR_PUPD5_0;

    /* SENSOR_RDY (PA1) — input */
    GPIOA->MODER &= ~GPIO_MODER_MODE1_Msk;

    /* VBAT_OK (PB1) — input */
    GPIOB->MODER &= ~GPIO_MODER_MODE1_Msk;

    /* RTC_INT (PA6) — input with falling-edge IRQ */
    GPIOA->MODER &= ~GPIO_MODER_MODE6_Msk;
    GPIOA->PUPDR &= ~GPIO_PUPDR_PUPD6_Msk;
    GPIOA->PUPDR |= GPIO_PUPDR_PUPD6_0;

    /* EXTI6 on PA6 for RTC alarm wake */
    SYSCFG->EXTICR[1] &= ~SYSCFG_EXTICR2_EXTI6;
    SYSCFG->EXTICR[1] |= SYSCFG_EXTICR2_EXTI6_PA;
    EXTI->IMR |= EXTI_IMR_IM6;
    EXTI->FTSR |= EXTI_FTSR_TR6;

    NVIC_EnableIRQ(EXTI4_15_IRQn);
}

/* ========================================================================
 *   Sleep mode (STOP with RTC alarm wake)
 * ======================================================================== */

static void enter_sleep(void) {
    GPIOA->BSRR = GPIO_BSRR_BR_7;

    /* Clear previous RTC alarm */
    pcf8523_clear_alarm();

    /* Set alarm to fire on the next matching minute */
    pcf8523_datetime_t dt;
    if (pcf8523_read_datetime(&dt)) {
        /* Alarm fires on this minute (already past), or next */
        pcf8523_set_minute_alarm((dt.minutes + 1) % 60);
    }

    /* Enter STOP mode */
    PWR->CR |= PWR_CR_LPSDSR;
    PWR->CR |= PWR_CR_ULP;
    SCB->SCR |= SCB_SCR_SLEEPDEEP_Msk;
    __WFI();

    /* Wake — LED on */
    GPIOA->BSRR = GPIO_BSRR_BS_7;
}

/* ========================================================================
 *   Measurement cycle
 * ======================================================================== */

static void do_measurement(void) {
    g_last_moisture_raw = fdc1004_read_raw(FDC1004_CIN1);
    g_last_moisture_pf  = fdc1004_read_pf(FDC1004_CIN1);

    if (g_sleep_cycles % FRAM_MEASURE_INTERVAL == 0) {
        uint16_t v_batt = bq25570_read_voltage_mv();
        uint16_t v_sense = (uint16_t)(g_last_moisture_pf * 10.0f);

        uint8_t status = 0;
        if (bq25570_vbat_ok()) status |= 0x01;
        if (st25dv04k_rf_present()) status |= 0x02;

        fram_ringbuffer_write(g_sleep_cycles, (uint16_t)g_last_moisture_raw,
                              v_batt, v_sense, status);
    }
}

/* ========================================================================
 *   NFC access
 * ======================================================================== */

static void handle_nfc_access(void) {
    uint16_t msg_len = st25dv04k_mailbox_read_len();
    if (msg_len > 0 && msg_len <= sizeof(g_nfc_buffer)) {
        st25dv04k_mailbox_read(g_nfc_buffer, &msg_len);

        uint8_t reply[16];
        reply[0] = 'M';
        reply[1] = (uint8_t)(g_last_moisture_raw >> 24);
        reply[2] = (uint8_t)(g_last_moisture_raw >> 16);
        reply[3] = (uint8_t)(g_last_moisture_raw >> 8);
        reply[4] = (uint8_t)(g_last_moisture_raw);
        st25dv04k_mailbox_write(reply, 5);
    }

    volatile uint32_t timeout = 1000000;
    while (st25dv04k_rf_present() && timeout--) {}
}

/* ========================================================================
 *   FRAM ring buffer
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

static bool fram_ringbuffer_write(uint32_t timestamp, uint16_t cap_raw,
                                   uint16_t v_batt, uint16_t v_sense,
                                   uint8_t status) {
    uint8_t entry[FRAM_ENTRY_SIZE];
    uint16_t addr;

    entry[0] = (uint8_t)(timestamp >> 24);
    entry[1] = (uint8_t)(timestamp >> 16);
    entry[2] = (uint8_t)(timestamp >> 8);
    entry[3] = (uint8_t)(timestamp);
    entry[4] = (uint8_t)(cap_raw >> 8);
    entry[5] = (uint8_t)(cap_raw);
    entry[6] = (uint8_t)(v_batt >> 8);
    entry[7] = (uint8_t)(v_batt);
    entry[8] = (uint8_t)(v_sense >> 8);
    entry[9] = (uint8_t)(v_sense);
    entry[10] = status;
    entry[11] = entry_crc(entry);

    addr = FRAM_DATA_START + g_fram_write_pos;

    /* Wrap around if we've hit the end */
    if (g_fram_entry_count >= FRAM_MAX_ENTRIES) {
        g_fram_write_pos = 0;
        addr = FRAM_DATA_START;
    }

    if (!mb85rc16_write(addr, entry, FRAM_ENTRY_SIZE)) {
        return false;
    }

    g_fram_write_pos += FRAM_ENTRY_SIZE;
    g_fram_entry_count++;

    /* Persist write pointer to header */
    uint8_t pos_buf[2];
    pos_buf[0] = (uint8_t)(g_fram_write_pos >> 8);
    pos_buf[1] = (uint8_t)(g_fram_write_pos);
    return mb85rc16_write(0x03, pos_buf, 2);
}

static uint8_t entry_crc(const uint8_t *data) {
    uint8_t crc = 0;
    for (int i = 0; i < FRAM_ENTRY_SIZE - 1; i++) {
        crc ^= data[i];
    }
    return crc;
}

/* ========================================================================
 *   Error logging (LED blink pattern)
 * ======================================================================== */

static void log_error(const char *msg) {
    (void)msg;
    g_app_state = APP_STATE_ERROR;
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
        /* Just wake — main loop handles everything */
    }
}