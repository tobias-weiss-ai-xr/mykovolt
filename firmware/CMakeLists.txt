cmake_minimum_required(VERSION 3.14)

project(mykovolt_firmware
    VERSION 0.1
    LANGUAGES C ASM
)

# ── Target ──
set(TARGET mykovolt_firmware)

# ── MCU settings ──
set(MCU_FAMILY    STM32L011xx)
set(MCU_CORE      cortex-m0plus)
set(FLASH_SIZE    16K)
set(RAM_SIZE      2K)

# ── Sources ──
set(CORE_SRC
    Core/Src/main.c
    Core/Src/i2c_driver.c
    Core/Src/fdc1004.c
    Core/Src/st25dv04k.c
)

set(STARTUP_SRC
    startup/startup_stm32l011xx.s
    Drivers/CMSIS/Device/ST/STM32L0xx/system_stm32l0xx.c
)

# ── Includes ──
set(CORE_INC
    Core/Inc
)

set(CMSIS_INC
    Drivers/CMSIS/Include
    Drivers/CMSIS/Device/ST/STM32L0xx/Include
)

set(HAL_INC
    Drivers/STM32L0xx_HAL_Driver/Inc
)

# ── Compile options ──
add_compile_options(
    -mcpu=${MCU_CORE}
    -mthumb
    -mfloat-abi=soft
    -ffunction-sections
    -fdata-sections
    -Wall
    -Wextra
    -Werror=implicit-function-declaration
    -Os
    -g
)

add_compile_definitions(
    ${MCU_FAMILY}
    HSE_VALUE=16000000
)

# ── Link options ──
add_link_options(
    -mcpu=${MCU_CORE}
    -mthumb
    -mfloat-abi=soft
    -specs=nano.specs
    -specs=nosys.specs
    -Wl,--gc-sections
    -Wl,-Map=${TARGET}.map
    -T${CMAKE_SOURCE_DIR}/startup/STM32L011F4Px.ld
)

# ── Build the executable ──
add_executable(${TARGET}
    ${CORE_SRC}
    ${STARTUP_SRC}
)

target_include_directories(${TARGET} PRIVATE
    ${CORE_INC}
    ${CMSIS_INC}
)

# ── Post-build: generate hex/bin ──
add_custom_command(TARGET ${TARGET} POST_BUILD
    COMMAND ${CMAKE_OBJCOPY} -O ihex ${TARGET} ${TARGET}.hex
    COMMAND ${CMAKE_SIZE} ${TARGET}
    COMMENT "Generating ${TARGET}.hex"
)

# ── Toolchain file path ──
set(CMAKE_TOOLCHAIN_FILE ${CMAKE_SOURCE_DIR}/cmake/arm-gcc-toolchain.cmake CACHE FILEPATH "ARM GCC toolchain")
