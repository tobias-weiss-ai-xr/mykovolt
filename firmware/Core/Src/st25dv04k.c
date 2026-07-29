/**
 * @file    st25dv04k.c
 * @brief   Driver for ST ST25DV04K dynamic NFC tag / I2C bridge
 *
 * 4Kbit EEPROM with I2C interface and ISO 15693 RF interface.
 * I2C address: 0x53
 *
 * The ST25DV04K uses 16-bit register addresses on the I2C bus.
 * Memory is organized as:
 *   0x0000–0x0CFF: System registers (configuration, security, mailbox)
 *   0x2000–0x21FF: User memory (512 bytes = 4 Kbit)
 *
 * Reference: ST ST25DV04K Datasheet (DocID030061)
 */

#include "st25dv04k.h"
#include "i2c_driver.h"
#include "mykovolt.h"
#include <stddef.h>

/* ── Mailbox constants ── */

#define ST25DV04K_MB_CTRL_INIT   0x02   /* Enable mailbox mode */
#define ST25DV04K_MB_MAX_LEN     255    /* Max mailbox message size (1-byte length field) */

/* ========================================================================
 *   Public API
 * ======================================================================== */

bool st25dv04k_init(void)
{
    /* ── Verify device is alive ── */
    uint8_t ic_ref = st25dv04k_read_ic_ref();
    if (ic_ref == 0xFF) {
        return false;  /* I2C error */
    }
    /* IC reference for ST25DV04K should be 0x24 */
    /* Accept 0x24 or any reasonable value — don't fail on unknown rev */

    /* ── Configure GPO as interrupt output ── */
    /* GPO register (0x0000):
     *   Bit 7: Enable interrupt on GPO pin
     *   Bit 0: RF activity detection
     * We enable both RF activity and interrupt output. */
    uint8_t gpo_cfg = ST25DV04K_GPO_INTERRUPT | ST25DV04K_GPO_RF_ACTIVE;

    if (!i2c_write_reg16(I2C_ADDR_ST25DV04K, ST25DV04K_REG_GPO, &gpo_cfg, 1)) {
        return false;
    }

    /* ── Enable mailbox mode ── */
    uint8_t mb_mode = ST25DV04K_MB_CTRL_INIT;
    if (!i2c_write_reg16(I2C_ADDR_ST25DV04K, ST25DV04K_REG_MB_MODE, &mb_mode, 1)) {
        return false;
    }

    /* ── Set mailbox watchdog to 1 second ── */
    uint8_t mb_wdg = 0x0A;  /* ~1 s with default prescaler */
    if (!i2c_write_reg16(I2C_ADDR_ST25DV04K, ST25DV04K_REG_MB_WDG, &mb_wdg, 1)) {
        return false;
    }

    return true;
}

bool st25dv04k_read_mem(uint16_t addr, uint8_t *data, uint16_t len)
{
    if (addr + len > ST25DV04K_USER_MEM_START + ST25DV04K_USER_MEM_SIZE) {
        return false;  /* Out of bounds */
    }
    return i2c_read_reg16(I2C_ADDR_ST25DV04K, addr, data, len);
}

bool st25dv04k_write_mem(uint16_t addr, const uint8_t *data, uint16_t len)
{
    if (addr + len > ST25DV04K_USER_MEM_START + ST25DV04K_USER_MEM_SIZE) {
        return false;  /* Out of bounds */
    }
    return i2c_write_reg16(I2C_ADDR_ST25DV04K, addr, data, len);
}

/* ========================================================================
 *   Mailbox
 * ======================================================================== */

uint16_t st25dv04k_mailbox_read_len(void)
{
    uint8_t len_byte = 0;
    if (!i2c_read_reg16(I2C_ADDR_ST25DV04K, ST25DV04K_REG_MB_LEN, &len_byte, 1)) {
        return 0;
    }
    return len_byte;
}

bool st25dv04k_mailbox_read(uint8_t *data, uint16_t *len)
{
    if (data == NULL || len == NULL || *len == 0) return false;

    uint16_t avail = st25dv04k_mailbox_read_len();
    if (avail == 0) {
        *len = 0;
        return true;  /* Nothing pending — not an error */
    }

    if (avail > *len) {
        avail = *len;  /* Clamp to caller's buffer size */
    }

    if (!i2c_read_reg16(I2C_ADDR_ST25DV04K, ST25DV04K_REG_MB_DATA, data, avail)) {
        return false;
    }

    *len = avail;
    return true;
}

bool st25dv04k_mailbox_write(const uint8_t *data, uint16_t len)
{
    if (data == NULL || len == 0 || len > ST25DV04K_MB_MAX_LEN) return false;

    /* Write message length byte */
    uint8_t len_byte = (uint8_t)len;
    if (!i2c_write_reg16(I2C_ADDR_ST25DV04K, ST25DV04K_REG_MB_LEN, &len_byte, 1)) {
        return false;
    }

    /* Write message data */
    if (!i2c_write_reg16(I2C_ADDR_ST25DV04K, ST25DV04K_REG_MB_DATA, data, len)) {
        return false;
    }

    return true;
}

/* ========================================================================
 *   RF Field Detection & Interrupts
 * ======================================================================== */

bool st25dv04k_rf_present(void)
{
    /* Read GPO configuration register — bit 0 indicates RF activity */
    uint8_t gpo;
    if (!i2c_read_reg16(I2C_ADDR_ST25DV04K, ST25DV04K_REG_GPO, &gpo, 1)) {
        return false;
    }
    return (gpo & ST25DV04K_GPO_RF_ACTIVE) != 0;
}

uint8_t st25dv04k_read_interrupt(void)
{
    /* Read the IT status register at 0x0001 (ITP) */
    uint8_t it_status;
    if (!i2c_read_reg16(I2C_ADDR_ST25DV04K, ST25DV04K_REG_ITP, &it_status, 1)) {
        return 0;
    }
    return it_status;
}

uint8_t st25dv04k_read_ic_ref(void)
{
    uint8_t ic_ref;
    if (!i2c_read_reg16(I2C_ADDR_ST25DV04K, ST25DV04K_REG_IC_REF, &ic_ref, 1)) {
        return 0xFF;
    }
    return ic_ref;
}
