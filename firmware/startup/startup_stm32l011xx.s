/**
 * @file    startup_stm32l011xx.s
 * @brief   STM32L011xx Startup File (Cortex-M0+)
 *
 * Reset vector, interrupt vector table, and initialization.
 * 16KB flash @ 0x08000000, 2KB RAM @ 0x20000000
 *
 * Adapted from STM32Cube L0 template.
 */

.syntax unified
.cpu    cortex-m0plus
.fpu    softvfp
.thumb

/* ── Memory addresses ── */
.equ  FLASH_BASE,    0x08000000
.equ  SRAM_BASE,     0x20000000
.equ  SRAM_SIZE,     0x00000800    /* 2KB */

/* Stack top: end of SRAM (grows downward) */
.equ  _estack,       SRAM_BASE + SRAM_SIZE

/* ── Section definitions ── */
.section  .vectors, "a", %progbits
.type     g_pfnVectors, %object
.size     g_pfnVectors, .-g_pfnVectors

g_pfnVectors:
  .word  _estack
  .word  Reset_Handler
  .word  NMI_Handler
  .word  HardFault_Handler
  .word  0                           /* Reserved */
  .word  0                           /* Reserved */
  .word  0                           /* Reserved */
  .word  0                           /* Reserved */
  .word  0                           /* Reserved */
  .word  0                           /* Reserved */
  .word  0                           /* Reserved */
  .word  SVC_Handler
  .word  0                           /* Reserved */
  .word  0                           /* Reserved */
  .word  PendSV_Handler
  .word  SysTick_Handler

  /* External interrupts (STM32L011: 16 lines) */
  .word  WWDG_IRQHandler             /* Window Watchdog */
  .word  PVD_IRQHandler              /* PVD through EXTI */
  .word  RTC_IRQHandler              /* RTC */
  .word  FLASH_IRQHandler            /* Flash */
  .word  RCC_IRQHandler              /* RCC */
  .word  EXTI0_1_IRQHandler          /* EXTI line 0-1 */
  .word  EXTI2_3_IRQHandler          /* EXTI line 2-3 */
  .word  EXTI4_15_IRQHandler         /* EXTI line 4-15 */
  .word  TIM21_IRQHandler            /* TIM21 */
  .word  TIM22_IRQHandler            /* TIM22 */
  .word  I2C1_IRQHandler             /* I2C1 */
  .word  SPI1_IRQHandler             /* SPI1 */
  .word  USART1_IRQHandler           /* USART1 */
  .word  USART2_IRQHandler           /* USART2 */
  .word  AES_RNG_LPUART1_IRQHandler  /* AES, RNG, LPUART1 */
  .word  ADC1_COMP_IRQHandler        /* ADC1, COMP1, COMP2 */

/* ── Reset handler ── */
.section  .text.Reset_Handler, "ax", %progbits
.type     Reset_Handler, %function
.global   Reset_Handler

Reset_Handler:
  /* Set stack pointer */
  ldr   r0, =_estack
  msr   msp, r0

  /* Clear BSS section */
  movs  r0, #0
  ldr   r1, =_sbss
  ldr   r2, =_ebss
  b     2f
1:
  str   r0, [r1]
  adds  r1, r1, #4
2:
  cmp   r1, r2
  bne   1b

  /* Copy data section from flash to RAM */
  ldr   r1, =_sidata
  ldr   r2, =_sdata
  ldr   r3, =_edata
  b     4f
3:
  ldr   r0, [r1]
  str   r0, [r2]
  adds  r1, r1, #4
  adds  r2, r2, #4
4:
  cmp   r2, r3
  bne   3b

  /* SystemInit (optional weak symbol) */
  bl    SystemInit

  /* Call constructors (C++ global objects) */
  bl    _init

  /* Branch to main */
  bl    main

  /* Infinite loop if main returns */
Loop:
  b     Loop

.size  Reset_Handler, .-Reset_Handler

/* ── Weak default handlers ── */
.section  .text.Default_Handler, "ax", %progbits

.macro  def_irq_handler  name
  .thumb_func
  .weak  \name
  .type  \name, %function
\name:
  b     .
  .size \name, .-\name
.endm

def_irq_handler  NMI_Handler
def_irq_handler  HardFault_Handler
def_irq_handler  SVC_Handler
def_irq_handler  PendSV_Handler
def_irq_handler  SysTick_Handler

def_irq_handler  WWDG_IRQHandler
def_irq_handler  PVD_IRQHandler
def_irq_handler  RTC_IRQHandler
def_irq_handler  FLASH_IRQHandler
def_irq_handler  RCC_IRQHandler
def_irq_handler  EXTI0_1_IRQHandler
def_irq_handler  EXTI2_3_IRQHandler
def_irq_handler  EXTI4_15_IRQHandler
def_irq_handler  TIM21_IRQHandler
def_irq_handler  TIM22_IRQHandler
def_irq_handler  I2C1_IRQHandler
def_irq_handler  SPI1_IRQHandler
def_irq_handler  USART1_IRQHandler
def_irq_handler  USART2_IRQHandler
def_irq_handler  AES_RNG_LPUART1_IRQHandler
def_irq_handler  ADC1_COMP_IRQHandler

/* ── Weak SystemInit ── */
.section  .text.SystemInit, "ax", %progbits
.weak     SystemInit
.type     SystemInit, %function
SystemInit:
  bx    lr
.size  SystemInit, .-SystemInit

/* ── Weak _init (C++ constructors) ── */
.section  .text._init, "ax", %progbits
.weak     _init
.type     _init, %function
_init:
  bx    lr
.size  _init, .-_init

.end
