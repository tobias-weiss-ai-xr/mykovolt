/**
 * @file    i2c_driver.c
 * @brief   I2C master driver for STM32L011 (bare-metal register access)
 *
 * Uses I2C1 peripheral on PA9 (SCL) and PA10 (SDA).
 * Standard mode 100kHz, 7-bit addressing.
 *
 * Reference: RM0385 (STM32L0x1 Reference Manual), Section 25
 */

#include "i2c_driver.h"
#include "mykovolt.h"

/* Register access */
#if !defined(GPIOA)
#error "This driver targets STM32L0 — check your MCU header"
#endif

/* ── Timing register values for 100kHz (HSI 16MHz) ── */
/* Computed with STM32CubeMX I2C Timing Calculator */
#define I2C_TIMINGR_100KHZ  0x00303D2B  /* PRESC=0, SCLDEL=3, SDADEL=1, SCLH=61, SCLL=107 */

/* ── State ── */
static volatile bool    i2c_busy = false;
static volatile uint32_t i2c_errors = 0;

/* ========================================================================
 *   Initialisation
 * ======================================================================== */

void i2c_init(void) {
    /* Enable I2C1 clock */
    RCC->APB1ENR |= RCC_APB1ENR_I2C1EN;

    /* Reset I2C1 */
    RCC->APB1RSTR |= RCC_APB1RSTR_I2C1RST;
    RCC->APB1RSTR &= ~RCC_APB1RSTR_I2C1RST;

    /* Configure GPIO: PA9=SCL(AF1), PA10=SDA(AF1), open-drain */
    GPIOA->MODER &= ~(GPIO_MODER_MODE9 | GPIO_MODER_MODE10);
    GPIOA->MODER = (GPIOA->MODER & ~(GPIO_MODER_MODE9 | GPIO_MODER_MODE10)) | GPIO_MODER_MODE9_1 | GPIO_MODER_MODE10_1;  /* AF = 0b10 */
    GPIOA->OTYPER |= GPIO_OTYPER_OT_9 | GPIO_OTYPER_OT_10; /* Open-drain */
    GPIOA->PUPDR &= ~(GPIO_PUPDR_PUPD9 | GPIO_PUPDR_PUPD10);
    GPIOA->PUPDR |= GPIO_PUPDR_PUPD9_0 | GPIO_PUPDR_PUPD10_0; /* Pull-up */
    GPIOA->AFR[1] &= ~(0xF << 4) & ~(0xF << 8);  /* AF1 for both */
    GPIOA->AFR[1] |= (1 << 4) | (1 << 8);         /* AF1 = I2C1 */

    /* Disable I2C before configuring */
    I2C1->CR1 &= ~I2C_CR1_PE;

    /* Set timing for 100kHz standard mode */
    I2C1->TIMINGR = I2C_TIMINGR_100KHZ;

    /* Enable I2C */
    I2C1->CR1 |= I2C_CR1_PE;

    i2c_busy = false;
    i2c_errors = 0;
}

void i2c_enable(void) {
    I2C1->CR1 |= I2C_CR1_PE;
}

void i2c_disable(void) {
    I2C1->CR1 &= ~I2C_CR1_PE;
}

bool i2c_ready(void) {
    return !i2c_busy && (I2C1->ISR & I2C_ISR_TXE);
}

uint32_t i2c_error_count(void) {
    return i2c_errors;
}

/* ========================================================================
 *   Wait for flag with timeout
 * ======================================================================== */

/**
 * Wait for an I2C ISR flag with a timeout.
 * @return true if flag set, false on timeout
 */
static bool wait_for_flag(uint32_t flag, bool set) {
    volatile uint32_t timeout = 50000;
    while (timeout--) {
        if (((I2C1->ISR & flag) != 0) == set) {
            return true;
        }
    }
    i2c_errors++;
    return false;
}

/* ========================================================================
 *   Master Transmit
 * ======================================================================== */

bool i2c_write_reg(uint8_t addr, uint8_t reg, const uint8_t *data, uint16_t len) {
    if (i2c_busy) return false;
    i2c_busy = true;

    /* Wait for bus ready */
    if (!wait_for_flag(I2C_ISR_BUSY, false)) {
        I2C1->ICR = 0xFFFFFFFF;  /* Clear all flags */
        i2c_busy = false;
        return false;
    }

    /* Start: send slave address + W */
    I2C1->CR2 = (addr << 1) | I2C_CR2_START;
    I2C1->CR2 |= (len + 1) | I2C_CR2_AUTOEND;  /* Nbytes = register + data */

    if (!wait_for_flag(I2C_ISR_TXIS, true)) {
        i2c_busy = false;
        return false;
    }

    /* Send register address */
    I2C1->TXDR = reg;

    /* Send data bytes */
    for (uint16_t i = 0; i < len; i++) {
        if (!wait_for_flag(I2C_ISR_TXIS, true)) {
            i2c_busy = false;
            return false;
        }
        I2C1->TXDR = data[i];
    }

    /* Wait for STOP (autoend) */
    if (!wait_for_flag(I2C_ISR_STOPF, true)) {
        i2c_busy = false;
        return false;
    }

    I2C1->ICR = I2C_ICR_STOPCF;
    i2c_busy = false;
    return true;
}

/* ========================================================================
 *   Master Receive
 * ======================================================================== */

bool i2c_read_reg(uint8_t addr, uint8_t reg, uint8_t *data, uint16_t len) {
    if (i2c_busy || len == 0) return false;
    i2c_busy = true;

    /* Wait for bus ready */
    if (!wait_for_flag(I2C_ISR_BUSY, false)) {
        I2C1->ICR = 0xFFFFFFFF;
        i2c_busy = false;
        return false;
    }

    /* Phase 1: Send register address (write) */
    I2C1->CR2 = (addr << 1) | I2C_CR2_START;
    I2C1->CR2 |= 1;  /* Send 1 byte (register address) */

    if (!wait_for_flag(I2C_ISR_TXIS, true)) {
        i2c_busy = false;
        return false;
    }
    I2C1->TXDR = reg;

    if (!wait_for_flag(I2C_ISR_TC, true)) {
        i2c_busy = false;
        return false;
    }

    /* Phase 2: Restart + read */
    I2C1->CR2 = (addr << 1) | I2C_CR2_START | I2C_CR2_RD_WRN;
    I2C1->CR2 |= len | I2C_CR2_AUTOEND;

    for (uint16_t i = 0; i < len; i++) {
        if (!wait_for_flag(I2C_ISR_RXNE, true)) {
            i2c_busy = false;
            return false;
        }
        data[i] = I2C1->RXDR;
    }

    /* Wait for STOP */
    if (!wait_for_flag(I2C_ISR_STOPF, true)) {
        i2c_busy = false;
        return false;
    }

    I2C1->ICR = I2C_ICR_STOPCF;
    i2c_busy = false;
    return true;
}

/* ========================================================================
 *   16-bit register address: Master Transmit
 * ======================================================================== */

bool i2c_write_reg16(uint8_t addr, uint16_t reg, const uint8_t *data, uint16_t len)
{
    if (i2c_busy) return false;
    i2c_busy = true;

    if (!wait_for_flag(I2C_ISR_BUSY, false)) {
        I2C1->ICR = 0xFFFFFFFF;
        i2c_busy = false;
        return false;
    }

    I2C1->CR2 = (addr << 1) | I2C_CR2_START;
    I2C1->CR2 |= (len + 2) | I2C_CR2_AUTOEND;

    if (!wait_for_flag(I2C_ISR_TXIS, true)) {
        i2c_busy = false;
        return false;
    }
    I2C1->TXDR = (uint8_t)(reg >> 8);

    if (!wait_for_flag(I2C_ISR_TXIS, true)) {
        i2c_busy = false;
        return false;
    }
    I2C1->TXDR = (uint8_t)(reg);

    for (uint16_t i = 0; i < len; i++) {
        if (!wait_for_flag(I2C_ISR_TXIS, true)) {
            i2c_busy = false;
            return false;
        }
        I2C1->TXDR = data[i];
    }

    if (!wait_for_flag(I2C_ISR_STOPF, true)) {
        i2c_busy = false;
        return false;
    }

    I2C1->ICR = I2C_ICR_STOPCF;
    i2c_busy = false;
    return true;
}

/* ========================================================================
 *   16-bit register address: Master Receive
 * ======================================================================== */

bool i2c_read_reg16(uint8_t addr, uint16_t reg, uint8_t *data, uint16_t len)
{
    if (i2c_busy || len == 0) return false;
    i2c_busy = true;

    if (!wait_for_flag(I2C_ISR_BUSY, false)) {
        I2C1->ICR = 0xFFFFFFFF;
        i2c_busy = false;
        return false;
    }

    /* Phase 1: Send 16-bit register address */
    I2C1->CR2 = (addr << 1) | I2C_CR2_START;
    I2C1->CR2 |= 2;

    if (!wait_for_flag(I2C_ISR_TXIS, true)) {
        i2c_busy = false;
        return false;
    }
    I2C1->TXDR = (uint8_t)(reg >> 8);

    if (!wait_for_flag(I2C_ISR_TXIS, true)) {
        i2c_busy = false;
        return false;
    }
    I2C1->TXDR = (uint8_t)(reg);

    if (!wait_for_flag(I2C_ISR_TC, true)) {
        i2c_busy = false;
        return false;
    }

    /* Phase 2: Restart + read */
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
