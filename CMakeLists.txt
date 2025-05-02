cmake_minimum_required(VERSION 3.12)

# Pull in Pico SDK (must be before project)
include(pico_sdk_import.cmake)

# We also need the Pimoroni libraries
include(pimoroni_pico_import.cmake)

project(picoclock C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# Initialize the Pico SDK
pico_sdk_init()

# Add executable
add_executable(picoclock
    pico-unicorn-clock/picoclock.cpp
)

# Enable USB output, disable UART output
pico_enable_stdio_usb(picoclock 1)
pico_enable_stdio_uart(picoclock 0)

# Add required libraries
target_link_libraries(picoclock 
    pico_stdlib
    hardware_spi
    hardware_pwm
    hardware_dma
    pico_unicorn
)

# Create map/bin/hex/uf2 file etc.
pico_add_extra_outputs(picoclock) 