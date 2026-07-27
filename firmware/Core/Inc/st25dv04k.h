/**
 * @file    st25dv04k.h
 * @brief   Driver for ST ST25DV04K dynamic NFC tag / I2C bridge
 *
 * 4Kbit EEPROM with I2C interface and ISO 15693 RF interface.
 * I2C address: 0x53
 * RF can read/write memory while I2C is active (mailbox mode).
 */

#ifndef __ST25DV04K_H
#define __ST25DV04K_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>

/* ── I2C Registers (memory-mapped) ── */

/* System configuration registers */
#define ST25DV04K_REG_GPO         0x0000  /* GPO configuration */
#define ST25DV04K_REG_ITP        0x0001  /* Interrupt pulse width */
#define ST25DV04K_REG_EH         0x0002  /* Energy harvesting */
#define ST25DV04K_REG_RF_MNGT    0x0003  /* RF management */
#define ST25DV04K_REG_RFA1SS     0x0004  /* RF area 1 security */
#define ST25DV04K_REG_RFA2SS     0x0005  /* RF area 2 security */
#define ST25DV04K_REG_RFA3SS     0x0006  /* RF area 3 security */
#define ST25DV04K_REG_RFA4SS     0x0007  /* RF area 4 security */
#define ST25DV04K_REG_DSF        0x0008  /* DSF ID */
#define ST25DV04K_REG_LOCK        0x0009  /* Lock configuration */
#define ST25DV04K_REG_MB_MODE    0x000A  /* Mailbox mode */
#define ST25DV04K_REG_MB_WDG     0x000B  /* Mailbox watchdog */
#define ST25DV04K_REG_LOCK_CFG   0x000C  /* Lock configuration */
#define ST25DV04K_REG_IC_REF     0x000D  /* IC reference */

/* Mailbox registers */
#define ST25DV04K_REG_MB_CTRL    0x0D00  /* Mailbox control */
#define ST25DV04K_REG_MB_LEN     0x0D01  /* Mailbox length */
#define ST25DV04K_REG_MB_DATA    0x0D02  /* Mailbox data (up to 256 bytes) */

/* User memory (4Kbit = 512 bytes, starting at 0x2000) */
#define ST25DV04K_USER_MEM_START 0x2000
#define ST25DV04K_USER_MEM_SIZE  512

/* ── GPO / IRQ configuration ── */

#define ST25DV04K_GPO_RF_ACTIVE   (1 << 0)  /* RF field detected */
#define ST25DV04K_GPO_MAILBOX     (1 << 1)  /* Mailbox message received */
#define ST25DV04K_GPO_RF_WRITE    (1 << 2)  /* RF write completed */
#define ST25DV04K_GPO_RF_PUT_MSG  (1 << 3)  /* RF put message */
#define ST25DV04K_GPO_RF_GET_MSG  (1 << 4)  /* RF get message */
#define ST25DV04K_GPO_INTERRUPT   (1 << 7)  /* Enable interrupt on GPO pin */

/* ── Public API ── */

/** Initialise the ST25DV04K (configure interrupts, etc.) */
bool st25dv04k_init(void);

/** Read bytes from user memory (I2C → tag) */
bool st25dv04k_read_mem(uint16_t addr, uint8_t *data, uint16_t len);

/** Write bytes to user memory (I2C → tag) */
bool st25dv04k_write_mem(uint16_t addr, const uint8_t *data, uint16_t len);

/** Read mailbox length (pending message size) */
uint16_t st25dv04k_mailbox_read_len(void);

/** Read mailbox data (message from RF reader) */
bool st25dv04k_mailbox_read(uint8_t *data, uint16_t *len);

/** Write to mailbox (message to RF reader) */
bool st25dv04k_mailbox_write(const uint8_t *data, uint16_t len);

/** Check if RF field is present */
bool st25dv04k_rf_present(void);

/** Check interrupt status (clears IRQ pin) */
uint8_t st25dv04k_read_interrupt(void);

/** Read IC type (should be 0x24 for ST25DV04K) */
uint8_t st25dv04k_read_ic_ref(void);

#ifdef __cplusplus
}
#endif

#endif /* __ST25DV04K_H */
