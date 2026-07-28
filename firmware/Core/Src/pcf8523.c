/**
 * @file    pcf8523.c
 * @brief   PCF8523 RTC driver
 *
 * Datasheet: NXP PCF8523, I2C RTC with alarm and countdown timer
 * Protocol: 7-bit addr 0x52, 8-bit register map
 */

#include "pcf8523.h"
#include "i2c_driver.h"
#include "mykovolt.h"

/* ── Helpers ── */

static uint8_t bcd_to_bin(uint8_t bcd) {
    return (bcd & 0x0F) + ((bcd >> 4) * 10);
}

static uint8_t bin_to_bcd(uint8_t bin) {
    return ((bin / 10) << 4) | (bin % 10);
}

/* ── Public API ── */

bool pcf8523_init(void) {
    uint8_t val;

    /* Read Control_1 */
    if (!i2c_read_reg(I2C_ADDR_PCF8523, PCF8523_REG_CTRL1, &val, 1)) {
        return false;
    }

    /* Clear STOP bit, set 24-hour mode */
    val &= ~PCF8523_CTRL1_STOP;
    val |= PCF8523_CTRL1_12_24;  /* 0 = 24h mode */
    if (!i2c_write_reg(I2C_ADDR_PCF8523, PCF8523_REG_CTRL1, &val, 1)) {
        return false;
    }

    /* Enable battery switch (Control_3: PM = 00 for BSM mode) */
    val = 0;
    if (!i2c_read_reg(I2C_ADDR_PCF8523, PCF8523_REG_CTRL3, &val, 1)) {
        return false;
    }
    val &= ~PCF8523_CTRL3_PM;
    if (!i2c_write_reg(I2C_ADDR_PCF8523, PCF8523_REG_CTRL3, &val, 1)) {
        return false;
    }

    return true;
}

void pcf8523_stop(void) {
    uint8_t val = 0;
    if (i2c_read_reg(I2C_ADDR_PCF8523, PCF8523_REG_CTRL1, &val, 1)) {
        val |= PCF8523_CTRL1_STOP;
        i2c_write_reg(I2C_ADDR_PCF8523, PCF8523_REG_CTRL1, &val, 1);
    }
}

void pcf8523_start(void) {
    uint8_t val = 0;
    if (i2c_read_reg(I2C_ADDR_PCF8523, PCF8523_REG_CTRL1, &val, 1)) {
        val &= ~PCF8523_CTRL1_STOP;
        i2c_write_reg(I2C_ADDR_PCF8523, PCF8523_REG_CTRL1, &val, 1);
    }
}

bool pcf8523_read_datetime(pcf8523_datetime_t *dt) {
    uint8_t buf[7];
    if (!i2c_read_reg(I2C_ADDR_PCF8523, PCF8523_REG_SECONDS, buf, 7)) {
        return false;
    }

    dt->seconds  = bcd_to_bin(buf[0] & 0x7F);
    dt->minutes  = bcd_to_bin(buf[1] & 0x7F);
    dt->hours    = bcd_to_bin(buf[2] & 0x3F);
    dt->days     = bcd_to_bin(buf[3] & 0x3F);
    dt->weekdays = bcd_to_bin(buf[4] & 0x07);
    dt->months   = bcd_to_bin(buf[5] & 0x1F);
    dt->years    = bcd_to_bin(buf[6]);
    return true;
}

bool pcf8523_set_datetime(const pcf8523_datetime_t *dt) {
    uint8_t buf[7];
    buf[0] = bin_to_bcd(dt->seconds) & 0x7F;
    buf[1] = bin_to_bcd(dt->minutes) & 0x7F;
    buf[2] = bin_to_bcd(dt->hours)   & 0x3F;
    buf[3] = bin_to_bcd(dt->days)    & 0x3F;
    buf[4] = bin_to_bcd(dt->weekdays) & 0x07;
    buf[5] = bin_to_bcd(dt->months)  & 0x1F;
    buf[6] = bin_to_bcd(dt->years);
    return i2c_write_reg(I2C_ADDR_PCF8523, PCF8523_REG_SECONDS, buf, 7);
}

bool pcf8523_set_minute_alarm(uint8_t minutes) {
    /* Enable alarm interrupt */
    uint8_t ctrl2 = PCF8523_CTRL2_AIE;
    if (!i2c_write_reg(I2C_ADDR_PCF8523, PCF8523_REG_CTRL2, &ctrl2, 1)) {
        return false;
    }

    /* Set minute alarm: AE=0 for minutes (match), AE=1 for others (ignore) */
    uint8_t minute_val = bin_to_bcd(minutes) & 0x7F;
    if (!i2c_write_reg(I2C_ADDR_PCF8523, PCF8523_REG_MINUTE_ALARM, &minute_val, 1)) {
        return false;
    }

    uint8_t ignore = PCF8523_ALARM_OFF;
    if (!i2c_write_reg(I2C_ADDR_PCF8523, PCF8523_REG_HOUR_ALARM, &ignore, 1)) {
        return false;
    }
    if (!i2c_write_reg(I2C_ADDR_PCF8523, PCF8523_REG_DAY_ALARM, &ignore, 1)) {
        return false;
    }
    if (!i2c_write_reg(I2C_ADDR_PCF8523, PCF8523_REG_WEEKDAY_ALARM, &ignore, 1)) {
        return false;
    }

    return true;
}

bool pcf8523_alarm_triggered(void) {
    uint8_t val = 0;
    if (!i2c_read_reg(I2C_ADDR_PCF8523, PCF8523_REG_CTRL2, &val, 1)) {
        return false;
    }
    return (val & PCF8523_CTRL2_AF) != 0;
}

void pcf8523_clear_alarm(void) {
    uint8_t val = PCF8523_CTRL2_AIE;
    i2c_write_reg(I2C_ADDR_PCF8523, PCF8523_REG_CTRL2, &val, 1);
}