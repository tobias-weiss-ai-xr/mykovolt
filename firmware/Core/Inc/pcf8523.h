/**
 * @file    pcf8523.h
 * @brief   PCF8523 RTC driver (I2C 0x52, 8-bit register map)
 */

#ifndef __PCF8523_H
#define __PCF8523_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>

/* ── Registers ── */

#define PCF8523_REG_CTRL1          0x00
#define PCF8523_REG_CTRL2          0x01
#define PCF8523_REG_CTRL3          0x02
#define PCF8523_REG_SECONDS        0x03
#define PCF8523_REG_MINUTES        0x04
#define PCF8523_REG_HOURS          0x05
#define PCF8523_REG_DAYS           0x06
#define PCF8523_REG_WEEKDAYS       0x07
#define PCF8523_REG_MONTHS         0x08
#define PCF8523_REG_YEARS          0x09
#define PCF8523_REG_MINUTE_ALARM   0x0A
#define PCF8523_REG_HOUR_ALARM     0x0B
#define PCF8523_REG_DAY_ALARM      0x0C
#define PCF8523_REG_WEEKDAY_ALARM  0x0D
#define PCF8523_REG_TS_LSB         0x0E
#define PCF8523_REG_TS_MSB         0x0F

/* ── Control bitfields ── */

/* Control_1 (0x00) */
#define PCF8523_CTRL1_12_24     (1 << 3)  /* 0=24h, 1=12h */
#define PCF8523_CTRL1_STOP      (1 << 5)  /* 1=stop RTC */

/* Control_2 (0x01) */
#define PCF8523_CTRL2_AIE       (1 << 1)  /* Alarm interrupt enable */
#define PCF8523_CTRL2_AF        (1 << 3)  /* Alarm flag (write 0 to clear) */

/* Control_3 (0x02) */
#define PCF8523_CTRL3_PM        (3 << 5)  /* Power management: 00=BSM, 01=direct, 10=battery, 11=direct */

/* Alarm registers: bit 7 = AEx (1 = disable this alarm field) */
#define PCF8523_ALARM_OFF       0x80

/* ── Datetime structure ── */

typedef struct {
    uint8_t seconds;  /* 0-59 */
    uint8_t minutes;  /* 0-59 */
    uint8_t hours;    /* 0-23 */
    uint8_t days;     /* 1-31 */
    uint8_t weekdays; /* 0-6 (Sun=0) */
    uint8_t months;   /* 1-12 */
    uint8_t years;    /* 0-99 */
} pcf8523_datetime_t;

/* ── Public API ── */

/** Initialise RTC: clear STOP, set 24h mode, enable battery switch */
bool pcf8523_init(void);

/** Stop/start the RTC */
void pcf8523_stop(void);
void pcf8523_start(void);

/** Read current date and time (returns false on I2C error) */
bool pcf8523_read_datetime(pcf8523_datetime_t *dt);

/** Set date and time */
bool pcf8523_set_datetime(const pcf8523_datetime_t *dt);

/** Enable alarm on minute match (set AE=0 for minute, AE=1 for hour/day/weekday) */
bool pcf8523_set_minute_alarm(uint8_t minutes);

/** Read alarm flag (true = alarm triggered) */
bool pcf8523_alarm_triggered(void);

/** Clear alarm flag */
void pcf8523_clear_alarm(void);

#ifdef __cplusplus
}
#endif

#endif /* __PCF8523_H */