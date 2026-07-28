/**
 * @file    bq25570.c
 * @brief   BQ25570 power management driver
 *
 * Datasheet: TI BQ25570, Nano-Power Boost Charger + LDO
 * The VBAT_OK pin (PB1) indicates the battery voltage is above the
 * programmed OK threshold. The LOAD_SW pin (PA4) controls the load
 * switch to the system.
 *
 * V_SENSE (PA0) provides battery voltage via resistor divider.
 * ADC conversion uses the STM32L011's built-in ADC1.
 */

#include "bq25570.h"
#include "mykovolt.h"

/* STM32L011xx.h is included via mykovolt.h */

/* ── Public API ── */

void bq25570_init(void) {
    /* VBAT_OK (PB1) configured as input in gpio_init() */

    /* Enable ADC1 clock */
    RCC->APB2ENR |= RCC_APB2ENR_ADC1EN;

    /* Calibrate ADC (required after power-on) */
    ADC1->CR |= ADC_CR_ADCAL;
    while (ADC1->CR & ADC_CR_ADCAL);

    /* Configure ADC: continuous mode disabled, 12-bit resolution */
    ADC1->CFGR1 &= ~ADC_CFGR1_CONT;
#if defined(ADC_CFGR1_RES_1)
    ADC1->CFGR1 &= ~ADC_CFGR1_RES_0;
    ADC1->CFGR1 |= ADC_CFGR1_RES_1;  /* 12-bit */
#endif

    /* Select V_SENSE channel (PA0 = ADC_IN0) */
    ADC1->CHSELR = ADC_CHSELR_CHSEL0;

    /* Enable ADC */
    ADC1->CR |= ADC_CR_ADEN;
    while (!(ADC1->ISR & ADC_ISR_ADRDY));
}

bool bq25570_vbat_ok(void) {
    return (GPIOB->IDR & PIN_VBAT_OK) != 0;
}

void bq25570_load_enable(void) {
    GPIOA->BSRR = GPIO_BSRR_BS_4;
}

void bq25570_load_disable(void) {
    GPIOA->BSRR = GPIO_BSRR_BR_4;
}

uint16_t bq25570_read_voltage_mv(void) {
    uint16_t raw;
    float volts;

    /* Start conversion */
    ADC1->CR |= ADC_CR_ADSTART;
    while (!(ADC1->ISR & ADC_ISR_EOC));

    /* Read result */
    raw = (uint16_t)(ADC1->DR & ADC_DR_DATA);

    /* Convert to mV: V_SENSE = V_DIVIDER / ratio
     * ADC range: 0-4095 = 0-VDDA (~1.8V from BQ25570 LDO)
     * Divider ratio: (R9 + R10) / R9 = (100k + 220k) / 100k = 3.2
     * Voltage = raw * 1800 / 4095 * 3.2 */
    volts = (float)raw * 1800.0f / 4095.0f * V_SENSE_DIVIDER_RATIO;

    return (uint16_t)volts;
}