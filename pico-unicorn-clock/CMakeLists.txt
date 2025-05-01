# CMakeLists.txt
cmake_minimum_required(VERSION 3.13)

# Change these paths if you cloned the SDK/libs elsewhere
set(PICO_SDK_PATH "/Users/charannanduri/Documents/VSCode/pico_deps/pico-sdk")
set(PIMORONI_PICO_PATH "/Users/charannanduri/Documents/VSCode/pico_deps/pimoroni-pico")

# Initialize SDK
include(${PICO_SDK_PATH}/pico_sdk_init.cmake)

project(pico_unicorn_clock_c C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# Initialize the Pico SDK
pico_sdk_init()

# Define Pimoroni Libraries Manually

# Hershey Fonts
add_library(hershey_fonts INTERFACE)
target_sources(hershey_fonts INTERFACE
    ${PIMORONI_PICO_PATH}/libraries/hershey_fonts/hershey_fonts.cpp
    ${PIMORONI_PICO_PATH}/libraries/hershey_fonts/hershey_fonts_data.cpp
)
target_include_directories(hershey_fonts INTERFACE
    ${PIMORONI_PICO_PATH}/libraries/hershey_fonts
    ${PIMORONI_PICO_PATH} # For common includes
)
# No explicit link dependencies for hershey_fonts itself based on its .cmake

# Bitmap Fonts
add_library(bitmap_fonts INTERFACE)
target_sources(bitmap_fonts INTERFACE
    ${PIMORONI_PICO_PATH}/libraries/bitmap_fonts/bitmap_fonts.cpp
)
target_include_directories(bitmap_fonts INTERFACE
    ${PIMORONI_PICO_PATH}/libraries/bitmap_fonts
    ${PIMORONI_PICO_PATH} # For common includes like unicode_sorta
)
# No explicit link dependencies for bitmap_fonts itself based on its .cmake

# Pico Graphics
add_library(pico_graphics INTERFACE)
target_sources(pico_graphics INTERFACE
    ${PIMORONI_PICO_PATH}/libraries/pico_graphics/types.cpp
    ${PIMORONI_PICO_PATH}/libraries/pico_graphics/pico_graphics.cpp
    ${PIMORONI_PICO_PATH}/libraries/pico_graphics/pico_graphics_pen_1bit.cpp
    ${PIMORONI_PICO_PATH}/libraries/pico_graphics/pico_graphics_pen_1bitY.cpp
    ${PIMORONI_PICO_PATH}/libraries/pico_graphics/pico_graphics_pen_3bit.cpp
    ${PIMORONI_PICO_PATH}/libraries/pico_graphics/pico_graphics_pen_p4.cpp
    ${PIMORONI_PICO_PATH}/libraries/pico_graphics/pico_graphics_pen_p8.cpp
    ${PIMORONI_PICO_PATH}/libraries/pico_graphics/pico_graphics_pen_rgb332.cpp
    ${PIMORONI_PICO_PATH}/libraries/pico_graphics/pico_graphics_pen_rgb565.cpp
    ${PIMORONI_PICO_PATH}/libraries/pico_graphics/pico_graphics_pen_rgb888.cpp
    ${PIMORONI_PICO_PATH}/libraries/pico_graphics/pico_graphics_pen_inky7.cpp
)
target_include_directories(pico_graphics INTERFACE
    ${PIMORONI_PICO_PATH}/libraries/pico_graphics
    ${PIMORONI_PICO_PATH} # For common includes
)
target_link_libraries(pico_graphics INTERFACE bitmap_fonts hershey_fonts pico_stdlib)

# Pico Unicorn
add_library(pico_unicorn INTERFACE)
pico_generate_pio_header(pico_unicorn ${PIMORONI_PICO_PATH}/libraries/pico_unicorn/pico_unicorn.pio)
target_sources(pico_unicorn INTERFACE
    ${PIMORONI_PICO_PATH}/libraries/pico_unicorn/pico_unicorn.cpp
)
target_include_directories(pico_unicorn INTERFACE
    ${PIMORONI_PICO_PATH}/libraries/pico_unicorn
    ${PIMORONI_PICO_PATH} # For common includes
)
target_link_libraries(pico_unicorn INTERFACE pico_stdlib pico_graphics hardware_pio hardware_dma)

# Add executable target
add_executable(${PROJECT_NAME}
        picoclock.cpp
        )

# Link necessary libraries for the final executable
target_link_libraries(${PROJECT_NAME}
        pico_stdlib
        hardware_pio # Added for Pico Unicorn dependency
        hardware_dma # Added for Pico Unicorn dependency
        pico_rand # For pico/rand.h
        # Link our manually defined interface libraries
        pico_graphics # Dependency of pico_unicorn
        pico_unicorn
        )

# Add include directories for our main executable (if needed)
# target_include_directories(${PROJECT_NAME} PUBLIC
#     ${PIMORONI_PICO_PATH} # Keep for relative includes like "common/.." if needed
#     )
# ^-- Probably not needed now as includes come via INTERFACE links

# Enable USB serial output
pico_enable_stdio_usb(${PROJECT_NAME} 1)
pico_enable_stdio_uart(${PROJECT_NAME} 0)

# Create map/bin/hex file etc.
pico_add_extra_outputs(${PROJECT_NAME})

# Add the uf2 target
pico_add_uf2_output(${PROJECT_NAME}) 