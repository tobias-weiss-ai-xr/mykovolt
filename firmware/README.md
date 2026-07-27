# MykoVolt DevKit Firmware

**MCU:** STM32L011F4Px (Cortex-M0+, 16KB Flash, 2KB RAM)  
**Toolchain:** ARM GCC + STM32CubeMX / CMake  
**Debug:** SWD via J1 (2×5 1.27mm SMD header)

## Peripherals (I²C Bus)

| Addr | Device | Function |
|------|--------|----------|
| 0x50 | MB85RC16 | 16Kbit FRAM (non-volatile storage) |
| 0x51 | FDC1004 | 4-channel capacitance sensor |
| 0x52 | PCF8523 | Real-time clock |
| 0x53 | ST25DV04K | NFC tag / dynamic I²C |

## Hardware Map

| STM32 Pin | Function | Connected To |
|-----------|----------|-------------|
| PA0 (6)   | ADC_IN   | V_SENSE (battery divider) |
| PA1 (7)   | GPIO-IN  | SENSOR_RDY (FDC1004) |
| PA2 (8)   | USART_TX | SWD header J1-8 |
| PA3 (9)   | USART_RX | SWD header J1-6 |
| PA4 (10)  | GPIO-OUT | LOAD_SW_GATE (Q1 gate) |
| PA5 (11)  | GPIO-IN  | NFC_IRQ (ST25DV04K) |
| PA6 (12)  | GPIO-IN  | RTC_INT (PCF8523) |
| PA7 (13)  | GPIO-OUT | MCU_LED_CTRL (LED2) |
| PA9 (17)  | I2C-SCL  | All I²C devices |
| PA10 (18) | I2C-SDA  | All I²C devices |
| PA13 (19) | SWD-SWDIO| SWD header J1-4 |
| PA14 (20) | SWD-SWCLK| SWD header J1-2 |
| PB1 (14)  | GPIO-IN  | VBAT_OK (BQ25570) |
| PB9 (1)   | GPIO     | (free / NFC_FD) |
| PC14 (2)  | OSC_IN   | 32.768kHz crystal |
| PC15 (3)  | OSC_OUT  | 32.768kHz crystal |
| NRST (4)  | RESET    | SWD header J1-10 |

## Power Architecture

```
Pressling (MFC) → J2 → BQ25570 (boost charger + LDO)
                            ├── VSTOR → SC1 (100mF supercap)
                            ├── VBAT_OK → STM32 PB1 (wake detect)
                            └── 3.3V → all ICs
                                         └── LED1 via Q1 (load switch)
```

## Directory Structure

```
firmware/
├── Core/
│   ├── Inc/          # Headers (main.h, i2c.h, drivers...)
│   └── Src/          # Source  (main.c, i2c.c, drivers...)
├── Drivers/
│   ├── STM32L0xx_HAL_Driver/   # ST HAL (if using CubeMX)
│   └── CMSIS/                  # ARM CMSIS core headers
├── startup/          # Startup code, linker script
├── CMakeLists.txt    # Build system
└── README.md         # This file
```

## Building

```bash
# Prerequisites: arm-none-eabi-gcc, cmake
cd firmware
mkdir build && cd build
cmake .. -DCMAKE_TOOLCHAIN_FILE=../cmake/arm-gcc-toolchain.cmake
make -j4
# Output: mykovolt_firmware.hex
```

## Programming

```bash
# Via ST-Link / SWD
openocd -f interface/stlink.cfg -f target/stm32l0.cfg \
  -c "program build/mykovolt_firmware.hex verify reset exit"
```
