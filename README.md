# Pico Unicorn Clock

A simple digital clock for the Raspberry Pi Pico with Pimoroni Pico Unicorn display.

![Pico Unicorn Clock](https://shop.pimoroni.com/cdn/shop/products/pico-unicorn-pack-on-2_1500x1500.jpg?v=1617369470)

## Features

- Digital clock displaying time in HH:MM format
- Colorful display with subtle color changes
- Low brightness for nighttime use & eye comfort
- Self-contained counter-based timekeeping (no RTC needed)
- RTC version is coming soon

## Hardware Requirements

- Raspberry Pi Pico
- Pimoroni Pico Unicorn Pack
- Micro USB cable

## Software Setup

### 1. Install required tools

#### For Windows:

1. Install [ARM GCC Toolchain](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads)
2. Install [CMake](https://cmake.org/download/)
3. Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) or use full Visual Studio
4. Install [Python 3](https://www.python.org/downloads/)
5. Install [Git](https://git-scm.com/download/win)

#### For macOS:

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required packages
brew install cmake
brew install python3
brew tap ArmMbed/homebrew-formulae
brew install arm-none-eabi-gcc
```

#### For Linux (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install cmake gcc-arm-none-eabi libnewlib-arm-none-eabi build-essential python3 python3-pip git
```

### 2. Set up the Raspberry Pi Pico SDK

```bash
# Create a development directory
mkdir ~/pico
cd ~/pico

# Clone the Pico SDK
git clone https://github.com/raspberrypi/pico-sdk.git
cd pico-sdk
git submodule update --init

# Set the PICO_SDK_PATH environment variable
# For Linux/macOS, add to ~/.bashrc or ~/.zshrc:
echo 'export PICO_SDK_PATH=~/pico/pico-sdk' >> ~/.bashrc
source ~/.bashrc

# For Windows, set environment variable in System Properties or via command:
# setx PICO_SDK_PATH "C:\path\to\pico-sdk"
```

### 3. Get Pimoroni Libraries

```bash
cd ~/pico
git clone https://github.com/pimoroni/pimoroni-pico.git
cd pimoroni-pico
git submodule update --init
```

## Building the Project

### 1. Clone this repository

```bash
cd ~/pico
git clone https://github.com/charannanduri/pico-unicorn-clock.git
cd pico-unicorn-clock
```



### 2. Create the build directory and build

Edit lines 143 & 144 of picoclock.cpp to the time youd like the clock to start at and save the file.
Then:

```bash
mkdir build
cd build
cmake .. -DPICO_SDK_PATH=~/pico/pico-sdk -DPIMORONI_PICO_PATH=~/pico/pimoroni-pico
make
```

This will generate a file with `.uf2` extension file in the build directory.

## Flashing to the Pico

1. Hold down the BOOTSEL button on the Pico
2. Connect the Pico to your computer via USB while holding the button
3. Release the BOOTSEL button after connecting
4. The Pico will mount as a USB mass storage device
5. Copy the `.uf2` file to the Pico drive
6. The Pico will automatically reboot and run the clock

## Building Your Own CMakeLists.txt

If you're starting from scratch, here's a CMakeLists.txt template for the project:

```cmake
cmake_minimum_required(VERSION 3.12)

# Initialize the Pico SDK
include(pico_sdk_import.cmake)

# Initialize the Pimoroni Pico library
include(pimoroni_pico_import.cmake)

project(picoclock C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

pico_sdk_init()

add_executable(picoclock
    picoclock.cpp
)

# Enable USB output, disable UART output
pico_enable_stdio_usb(picoclock 1)
pico_enable_stdio_uart(picoclock 0)

# Add pico_stdlib library which aggregates commonly used features
target_link_libraries(picoclock 
    pico_stdlib
    hardware_spi
    hardware_pwm
    hardware_dma
    pico_unicorn
)

# Create map/bin/hex/uf2 file etc.
pico_add_extra_outputs(picoclock)
```

Don't forget to include the necessary import files from the SDK and Pimoroni libraries.

## Customizing the Clock

- To change the initial time, modify the `current_hour` and `current_minute` variables in `picoclock.cpp`
- To adjust brightness, modify the RGB values in the color generation code
- To change the update interval, modify the `sleep_ms()` value (default is 60000ms or 1 minute)

## Troubleshooting

### Code doesn't compile

- Check that `PICO_SDK_PATH` is set correctly
- Ensure you've initialized the Pico SDK submodules
- Verify that the Pimoroni libraries are installed correctly

### Pico doesn't appear as a drive when pressing BOOTSEL

- Try a different USB cable
- Connect directly to your computer (not through a hub)
- Check that the cable supports data transfer (not power-only)

### Pico is connected but no display

- Check that the Pico Unicorn is seated properly on the Pico
- Verify that the code was compiled and flashed correctly 
- Try reinstalling the firmware by holding BOOTSEL and flashing again

## License

MIT License

## Acknowledgments

- [Raspberry Pi Pico Documentation](https://www.raspberrypi.org/documentation/pico/getting-started/)
- [Pimoroni Pico Libraries](https://github.com/pimoroni/pimoroni-pico) 