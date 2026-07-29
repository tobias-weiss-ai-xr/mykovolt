cmake_minimum_required(VERSION 3.14)

project(mykovolt_testfixture
    VERSION 0.1
    LANGUAGES C ASM
)

set(TARGET mykovolt_testfixture)

set(MCU_FAMILY    STM32L011xx)
set(MCU_CORE      cortex-m0plus)
set(FLASH_SIZE    16K)
set(RAM_SIZE      2K)

set(CORE_SRC
    ${CMAKE_CURRENT_SOURCE_DIR}/testfixture_main.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../Core/Src/i2c_driver.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../Core/Src/ina219.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../Core/Src/sht30.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../Core/Src/st25dv04k.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../Core/Src/mb85rc16.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../Core/Src/pcf8523.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../Core/Src/bq25570.c
)

set(STARTUP_SRC
    ${CMAKE_CURRENT_SOURCE_DIR}/../startup/startup_stm32l011xx.s
    ${CMAKE_CURRENT_SOURCE_DIR}/../Drivers/CMSIS/Device/ST/STM32L0xx/system_stm32l0xx.c
)

set(CORE_INC
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/../Core/Inc
)

set(CMSIS_INC
    ${CMAKE_CURRENT_SOURCE_DIR}/../Drivers/CMSIS/Include
    ${CMAKE_CURRENT_SOURCE_DIR}/../Drivers/CMSIS/Device/ST/STM32L0xx/Include
)

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

add_link_options(
    -mcpu=${MCU_CORE}
    -mthumb
    -mfloat-abi=soft
    -specs=nano.specs
    -specs=nosys.specs
    -Wl,--gc-sections
    -Wl,-Map=${TARGET}.map
    -T${CMAKE_CURRENT_SOURCE_DIR}/../startup/STM32L011F4Px.ld
)

add_executable(${TARGET}
    ${CORE_SRC}
    ${STARTUP_SRC}
)

target_include_directories(${TARGET} PRIVATE
    ${CORE_INC}
    ${CMSIS_INC}
)

add_custom_command(TARGET ${TARGET} POST_BUILD
    COMMAND ${CMAKE_OBJCOPY} -O ihex ${TARGET} ${TARGET}.hex
    COMMAND ${CMAKE_SIZE} ${TARGET}
    COMMENT "Generating ${TARGET}.hex"
)

set(CMAKE_TOOLCHAIN_FILE ${CMAKE_CURRENT_SOURCE_DIR}/../cmake/arm-gcc-toolchain.cmake CACHE FILEPATH "ARM GCC toolchain")
