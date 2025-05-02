# This file can be dropped into a project to help locate the Pimoroni Pico libraries
# It will also set up the required include and module search paths

if (DEFINED ENV{PIMORONI_PICO_PATH} AND (NOT PIMORONI_PICO_PATH))
    set(PIMORONI_PICO_PATH $ENV{PIMORONI_PICO_PATH})
    message("Using PIMORONI_PICO_PATH from environment ('${PIMORONI_PICO_PATH}')")
endif ()

if (NOT PIMORONI_PICO_PATH)
    # If PIMORONI_PICO_PATH not set, assume the library is located one directory above
    get_filename_component(PIMORONI_PICO_PATH "${CMAKE_CURRENT_LIST_DIR}/.." REALPATH)
    if (NOT EXISTS ${PIMORONI_PICO_PATH}/pimoroni_pico)
        message(FATAL_ERROR "Directory '${PIMORONI_PICO_PATH}/pimoroni_pico' not found. Please set PIMORONI_PICO_PATH.")
    endif()
endif ()

set(PIMORONI_PICO_PATH "${PIMORONI_PICO_PATH}" CACHE PATH "Path to the Pimoroni Pico libraries")

# Check if Pimoroni Pico SDK exists
if (NOT EXISTS ${PIMORONI_PICO_PATH}/common)
    message(FATAL_ERROR "Directory '${PIMORONI_PICO_PATH}/common' not found. Please set PIMORONI_PICO_PATH.")
endif()

# Add the common include directory to our search path
include_directories(${PIMORONI_PICO_PATH})

# Add specific libraries needed for Pico Unicorn
include_directories(${PIMORONI_PICO_PATH}/libraries/pico_unicorn)
add_subdirectory(${PIMORONI_PICO_PATH}/libraries/pico_unicorn pico_unicorn) 