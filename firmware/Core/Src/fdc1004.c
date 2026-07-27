/**
 * @file    fdc1004.c
 * @brief   Driver for TI FDC1004 4-channel capacitance-to-digital converter
 *
 * I2C address: 0x51 (ADDR = VDD via 10kΩ)
 * Reference: TI FDC1004 Datasheet (SNOSCY6)
 *
 * The FDC1004 measures capacitance with 24-bit resolution across a
 * configurable full-scale range (±15 pF default). Results are stored
 * in offset-binary format.
 */

#include "fdc1004.h"
#include "i2c_driver.h"
#include "mykovolt.h"

/* ── Register bitfield helpers ── */

/* CONF_MSB (0x08) bits */
#define FDC1004_CONF_DONE       (1 << 15)   /* Measurement complete */
#define FDC1004_CONF_AMUX_MASK  (7 << 13)   /* AMUX select */
#define FDC1004_CONF_RATE_MASK  (3 << 8)    /* Measurement rate */

/* ── Conversion constants ── */

/** Full-scale capacitance range in pF (±15 pF) */
#define FDC1004_FULL_SCALE_PF   30.0f

/** Number of bits in the ADC conversion result */
#define FDC1004_ADC_BITS        24

/** LSB weight in fF: 30 pF / 2^24 ≈ 1.788 fF */
#define FDC1004_LSB_FF          ((FDC1004_FULL_SCALE_PF * 1000.0f) / (float)(1UL << FDC1004_ADC_BITS))

/** Offset-binary zero point (0 pF) */
#define FDC1004_OFFSET_BINARY   (1UL << (FDC1004_ADC_BITS - 1))

/* ========================================================================
 *   Helper: read a 16-bit register (MSB first)
 * ======================================================================== */

static uint16_t read_u16(uint8_t reg)
{
    uint8_t buf[2];
    if (!i2c_read_reg(I2C_ADDR_FDC1004, reg, buf, 2)) {
        return 0xFFFF;
    }
    return ((uint16_t)buf[0] << 8) | buf[1];
}

/* ========================================================================
 *   Helper: write a 16-bit register (MSB first)
 * ======================================================================== */

static bool write_u16(uint8_t reg, uint16_t val)
{
    uint8_t buf[2];
    buf[0] = (uint8_t)(val >> 8);
    buf[1] = (uint8_t)(val);
    return i2c_write_reg(I2C_ADDR_FDC1004, reg, buf, 2);
}

/* ========================================================================
 *   Public API
 * ======================================================================== */

bool fdc1004_init(void)
{
    /* Reset the device: pulse RESET bit in CONF via a full 16-bit write.
     * The FDC1004 does not have a dedicated reset register, but writing
     * a known-good configuration achieves the same effect. */

    /* Configure: 100 Hz measurement rate, AMUX disabled */
    uint16_t conf = FDC1004_MEAS_RATE_100HZ | FDC1004_AMUX_DISABLED;
    if (!write_u16(FDC1004_REG_CONF_MSB, conf)) {
        return false;
    }

    /* Verify the device is alive by reading the manufacturer ID */
    uint16_t manuf = read_u16(FDC1004_REG_MANUFACTURER_ID);
    if (manuf == 0xFFFF) {
        return false;  /* I2C error */
    }
    /* 0x5449 = "TI" in ASCII */
    if (manuf != 0x5449) {
        return false;  /* Unexpected ID — wrong device or address */
    }

    return true;
}

int32_t fdc1004_read_raw(uint8_t channel)
{
    if (channel > 3) return 0;

    uint8_t reg_msb = FDC1004_REG_CIN1_MSB + channel * 2;
    uint8_t reg_lsb = FDC1004_REG_CIN1_LSB + channel * 2;

    /* Read the 16-bit MSB register (upper 16 bits of the 24-bit result) */
    uint16_t msb = read_u16(reg_msb);
    /* Read the 16-bit LSB register (lower 8 bits of the 24-bit result in bits[15:8]) */
    uint16_t lsb = read_u16(reg_lsb);

    /* Reconstruct the 24-bit offset-binary value:
     *   result[23:0] = (MSB << 8) | (LSB >> 8)
     * MSB contains bits [23:8], LSB contains bits [7:0] in its upper byte. */
    uint32_t raw24 = ((uint32_t)msb << 8) | (lsb >> 8);

    /* Convert from offset binary to signed */
    return (int32_t)(raw24 - FDC1004_OFFSET_BINARY);
}

float fdc1004_read_pf(uint8_t channel)
{
    int32_t raw = fdc1004_read_raw(channel);

    /* Capacitance (pF) = raw * (full_scale / 2^24)
     * full_scale = ±15 pF → 30 pF range
     * raw is the signed offset from 0 pF */
    return (float)raw * FDC1004_LSB_FF / 1000.0f;
}

bool fdc1004_is_ready(void)
{
    uint16_t conf = read_u16(FDC1004_REG_CONF_MSB);
    if (conf == 0xFFFF) return false;  /* I2C error */
    return (conf & FDC1004_CONF_DONE) != 0;
}

int16_t fdc1004_read_offset(uint8_t channel)
{
    if (channel > 3) return 0;
    uint16_t val = read_u16(FDC1004_REG_OFFSET_CIN1 + channel);
    return (int16_t)val;
}

uint16_t fdc1004_read_gain(uint8_t channel)
{
    if (channel > 3) return 0;
    return read_u16(FDC1004_REG_GAIN_CIN1 + channel);
}

uint16_t fdc1004_read_manufacturer_id(void)
{
    return read_u16(FDC1004_REG_MANUFACTURER_ID);
}

uint16_t fdc1004_read_device_id(void)
{
    return read_u16(FDC1004_REG_DEVICE_ID);
}
