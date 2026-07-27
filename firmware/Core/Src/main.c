/**
 * @file    main.c
 * @brief   MykoVolt DevKit — main application
 *
 * ── System Overview ──
 *   MCU:      STM32L011F4 (Cortex-M0+, 16MHz, 16KB flash, 2KB RAM)
 *   Power:    BQ25570 (boost charger + LDO from pressling MFC)
 *   Storage:  MB85RC16 (16Kbit FRAM, I2C 0x50)
 *   Sensor:   FDC1004 (4ch capacitance, I2C 0x51)
 *   RTC:      PCF8523 (I2C 0x52)
 *   NFC:      ST25DV04K (I2C 0x53 + RF ISO 15693)
 *
 * ── Application States ──
 *   SLEEP ──> ACTIVE ──> SLEEP  (duty-cycled measurement)
 *              └──> NFC_ACCESS   (when RF field detected)
 */

#include "mykovolt.h"
#include "i2c_driver.h"
#include "fdc1004.h"
#include "st25dv04k.h"

#include <string.h>

/* ========================================================================
 *   Local state
 * ======================================================================== */

static app_state_t g_app_state = APP_STATE_SLEEP;
static uint32_t    g_sleep_cycles = 0;      /* Number of sleep cycles */
static int32_t     g_last_moisture_raw = 0; /* Last FDC1004 reading */
static float       g_last_moisture_pf = 0.0f;
static uint8_t     g_nfc_buffer[128];       /* Buffer for NFC mailbox */

/* ========================================================================
 *   Forward declarations
 * ======================================================================== */

static void system_clock_init(void);
static void gpio_init(void);
static void enter_sleep(void);
static void do_measurement(void);
static void handle_nfc_access(void);
static void log_error(const char *msg);

/* ========================================================================
 *   main
 * ======================================================================== */

int main(void) {
    /* ── System initialisation ── */
    system_clock_init();
    gpio_init();
    i2c_init();

    /* ── Peripheral initialisation ── */
    if (!fdc1004_init()) {
        log_error("FDC1004 init failed");
    }

    if (!st25dv04k_init()) {
        log_error("ST25DV04K init failed");
    }

    /* Read device IDs for verification (unused in release, kept for debug) */
    (void)fdc1004_read_device_id();
    (void)st25dv04k_read_ic_ref();

    /* ── Main loop ── */
    while (1) {
        switch (g_app_state) {
        case APP_STATE_SLEEP:
            /* Check for NFC field — if present, skip sleep */
            if (st25dv04k_rf_present()) {
                g_app_state = APP_STATE_NFC_ACCESS;
                break;
            }
            enter_sleep();
            g_sleep_cycles++;
            g_app_state = APP_STATE_ACTIVE;
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
            /* Blink error LED, then reset to sleep */
            for (volatile int i = 0; i < 1000000; i++);
            g_app_state = APP_STATE_SLEEP;
            break;
        }
    }
}

/* ========================================================================
 *   System clock: HSI 16MHz, no PLL
 * ======================================================================== */

static void system_clock_init(void) {
    /* Enable HSI */
    RCC->CR |= RCC_CR_HSION;
    while (!(RCC->CR & RCC_CR_HSIRDY));

    /* Select HSI as system clock */
    RCC->CFGR = (RCC->CFGR & ~RCC_CFGR_SW) | RCC_CFGR_SW_HSI;
    while ((RCC->CFGR & RCC_CFGR_SWS) != RCC_CFGR_SWS_HSI);

    /* Set AHB/APB prescalers (1:1) */
    RCC->CFGR &= ~(RCC_CFGR_HPRE | RCC_CFGR_PPRE1 | RCC_CFGR_PPRE2);

    /* Enable LSE for RTC (if available) */
    RCC->CSR |= RCC_CSR_LSEON;
}

/* ========================================================================
 *   GPIO
 * ======================================================================== */

static void gpio_init(void) {
    /* Enable GPIO clocks */
    RCC->IOPENR |= RCC_IOPENR_GPIOAEN | RCC_IOPENR_GPIOBEN | RCC_IOPENR_GPIOCEN;

    /* LED2 (PA7) — push-pull output */
    GPIOA->MODER &= ~GPIO_MODER_MODE7_Msk;
    GPIOA->MODER |= GPIO_MODER_MODE7_0;  /* Output */
    GPIOA->OTYPER &= ~GPIO_OTYPER_OT_7;   /* Push-pull */
    GPIOA->PUPDR &= ~GPIO_PUPDR_PUPD7_Msk;

    /* LOAD_SW_GATE (PA4) — push-pull output, initially on */
    GPIOA->MODER &= ~GPIO_MODER_MODE4_Msk;
    GPIOA->MODER |= GPIO_MODER_MODE4_0;
    GPIOA->OTYPER &= ~GPIO_OTYPER_OT_4;
    GPIOA->PUPDR &= ~GPIO_PUPDR_PUPD4_Msk;
    GPIOA->BSRR = GPIO_BSRR_BS_4;  /* Turn on load switch */

    /* NFC IRQ (PA5) — input with pull-up */
    GPIOA->MODER &= ~GPIO_MODER_MODE5_Msk;
    GPIOA->PUPDR &= ~GPIO_PUPDR_PUPD5_Msk;
    GPIOA->PUPDR |= GPIO_PUPDR_PUPD5_0;  /* Pull-up */

    /* SENSOR_RDY (PA1) — input */
    GPIOA->MODER &= ~GPIO_MODER_MODE1_Msk;

    /* VBAT_OK (PB1) — input */
    GPIOB->MODER &= ~GPIO_MODER_MODE1_Msk;

    /* RTC_INT (PA6) — input */
    GPIOA->MODER &= ~GPIO_MODER_MODE6_Msk;
}

/* ========================================================================
 *   Sleep mode (STOP with RTC wake)
 * ======================================================================== */

static void enter_sleep(void) {
    /* Set LED off */
    GPIOA->BSRR = GPIO_BSRR_BR_7;

    /* Enter STOP mode */
    PWR->CR |= PWR_CR_LPSDSR;    /* Low-power run in STOP */
    PWR->CR |= PWR_CR_ULP;       /* Ultra-low power */
    SCB->SCR |= SCB_SCR_SLEEPDEEP_Msk;
    __WFI();

    /* Wake up — LED on */
    GPIOA->BSRR = GPIO_BSRR_BS_7;
}

/* ========================================================================
 *   Measurement cycle
 * ======================================================================== */

static void do_measurement(void) {
    /* ── Read soil moisture (CIN1) ── */
    g_last_moisture_raw = fdc1004_read_raw(FDC1004_CIN1);
    g_last_moisture_pf  = fdc1004_read_pf(FDC1004_CIN1);

    /* ── Store to FRAM (every 10th cycle) ── */
    if (g_sleep_cycles % 10 == 0) {
        uint8_t buf[4];
        buf[0] = (uint8_t)(g_sleep_cycles >> 24);
        buf[1] = (uint8_t)(g_sleep_cycles >> 16);
        buf[2] = (uint8_t)(g_sleep_cycles >> 8);
        buf[3] = (uint8_t)(g_sleep_cycles);
        /* FRAM write would go here via i2c_write_reg8(I2C_ADDR_FRAM, ...) */
        (void)buf;
    }
}

/* ========================================================================
 *   NFC access
 * ======================================================================== */

static void handle_nfc_access(void) {
    /* Read any pending mailbox message from the NFC reader */
    uint16_t msg_len = st25dv04k_mailbox_read_len();
    if (msg_len > 0 && msg_len <= sizeof(g_nfc_buffer)) {
        st25dv04k_mailbox_read(g_nfc_buffer, &msg_len);

        /* Echo latest sensor reading into mailbox for RF reader */
        uint8_t reply[16];
        reply[0] = 'M';  /* 'M' = moisture data */
        reply[1] = (uint8_t)(g_last_moisture_raw >> 24);
        reply[2] = (uint8_t)(g_last_moisture_raw >> 16);
        reply[3] = (uint8_t)(g_last_moisture_raw >> 8);
        reply[4] = (uint8_t)(g_last_moisture_raw);
        st25dv04k_mailbox_write(reply, 5);
    }

    /* Wait for RF field to disappear */
    volatile uint32_t timeout = 1000000;
    while (st25dv04k_rf_present() && timeout--) {
        /* Spin — in production, use a timer */
    }
}

/* ========================================================================
 *   Error logging (LED blink pattern)
 * ======================================================================== */

static void log_error(const char *msg) {
    (void)msg;
    g_app_state = APP_STATE_ERROR;
    /* Blink LED 3 times */
    for (int i = 0; i < 3; i++) {
        GPIOA->BSRR = GPIO_BSRR_BS_7;
        for (volatile int j = 0; j < 200000; j++);
        GPIOA->BSRR = GPIO_BSRR_BR_7;
        for (volatile int j = 0; j < 200000; j++);
    }
}
