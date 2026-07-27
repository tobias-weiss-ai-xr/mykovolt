# ARM GCC toolchain file for STM32L0
set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR arm)

set(CMAKE_C_COMPILER   arm-none-eabi-gcc)
set(CMAKE_CXX_COMPILER arm-none-eabi-g++)
set(CMAKE_ASM_COMPILER arm-none-eabi-gcc)
set(CMAKE_OBJCOPY      arm-none-eabi-objcopy)
set(CMAKE_OBJDUMP      arm-none-eabi-objdump)
set(CMAKE_SIZE         arm-none-eabi-size)
set(CMAKE_DEBUGGER     arm-none-eabi-gdb)

set(CMAKE_C_FLAGS   "-mcpu=cortex-m0plus -mthumb -mfloat-abi=soft" CACHE STRING "" FORCE)
set(CMAKE_CXX_FLAGS "-mcpu=cortex-m0plus -mthumb -mfloat-abi=soft" CACHE STRING "" FORCE)
set(CMAKE_ASM_FLAGS "-mcpu=cortex-m0plus -mthumb" CACHE STRING "" FORCE)
