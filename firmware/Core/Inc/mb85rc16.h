/**
 * @file    mb85rc16.h
 * @brief   MB85RC16 FRAM driver (16Kbit, I2C 0x50, 16-bit addressing)
 */

#ifndef __MB85RC16_H
#define __MB85RC16_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>

/* ── Constants ── */

#define MB85RC16_SIZE         2048  /* 16Kbit = 2KB */
#define MB85RC16_PAGE_SIZE    4     /* Max bytes per write */
#define MB85RC16_ADDR_MAX     0x07FF

/* ── Public API ── */

/** Initialise FRAM (verifies device presence) */
bool mb85rc16_init(void);

/** Read a single byte from a 16-bit memory address (returns 0xFF on error) */
uint8_t mb85rc16_read_byte(uint16_t addr);

/** Read multiple bytes into a buffer (returns bytes read, 0 on error) */
uint16_t mb85rc16_read(uint16_t addr, uint8_t *buf, uint16_t len);

/** Write a single byte (returns true on success) */
bool mb85rc16_write_byte(uint16_t addr, uint8_t val);

/** Write multiple bytes (returns true on success) */
bool mb85rc16_write(uint16_t addr, const uint8_t *data, uint16_t len);

#ifdef __cplusplus
}
#endif

#endif /* __MB85RC16_H */