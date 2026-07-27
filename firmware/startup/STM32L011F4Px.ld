/**
 * @file    STM32L011F4Px.ld
 * @brief   Linker script for STM32L011F4Px (Cortex-M0+)
 *
 * Memory map:
 *   FLASH: 0x08000000 - 0x08003FFF  (16KB)
 *   SRAM:  0x20000000 - 0x200007FF  (2KB)
 */

MEMORY
{
  FLASH  (rx)  : ORIGIN = 0x08000000, LENGTH = 16K
  RAM    (rw)  : ORIGIN = 0x20000000, LENGTH = 2K
}

/* ── Stack and heap sizes ── */
_stack_size  = 0x200;    /* 512 bytes */
_heap_size   = 0x100;    /* 256 bytes  */

/* ── Section layout ── */
SECTIONS
{
  /* Vector table at start of flash */
  .vectors :
  {
    . = ALIGN(4);
    _svectors = .;
    KEEP(*(.vectors))
    _evectors = .;
  } > FLASH

  /* Code + read-only data */
  .text :
  {
    . = ALIGN(4);
    _stext = .;
    *(.text*)
    *(.rodata*)
    *(.glue_7)
    *(.glue_7t)
    KEEP(*(.init))
    KEEP(*(.fini))
    . = ALIGN(4);
    _etext = .;
  } > FLASH

  /* ARM exception index table */
  .ARM.exidx :
  {
    *(.ARM.exidx*)
  } > FLASH

  /* Initialized data (copied from flash to RAM at startup) */
  . = ALIGN(4);
  _sidata = .;

  .data : AT(_sidata)
  {
    . = ALIGN(4);
    _sdata = .;
    *(.data*)
    . = ALIGN(4);
    _edata = .;
  } > RAM

  /* Zero-initialized data */
  .bss :
  {
    . = ALIGN(4);
    _sbss = .;
    *(.bss*)
    *(COMMON)
    . = ALIGN(4);
    _ebss = .;
  } > RAM

  /* Heap */
  .heap :
  {
    . = ALIGN(8);
    _sheap = .;
    . = . + _heap_size;
    . = ALIGN(8);
    _eheap = .;
  } > RAM

  /* Stack (grows downward from end of RAM) */
  .stack :
  {
    . = ALIGN(8);
    _sstack = .;
    . = . + _stack_size;
    . = ALIGN(8);
    _estack = .;
  } > RAM

  /* Discard unused sections */
  /DISCARD/ :
  {
    *(.comment)
    *(.note.*)
    *(.ARM.attributes)
  }
}

/* ── Exported symbols ── */
PROVIDE(_sflash = ORIGIN(FLASH));
PROVIDE(_eflash = ORIGIN(FLASH) + LENGTH(FLASH));
PROVIDE(_sram   = ORIGIN(RAM));
PROVIDE(_eram   = ORIGIN(RAM) + LENGTH(RAM));
