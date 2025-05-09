# CircuitPython Board Configuration System

This document describes the new board configuration system for CircuitPython, which allows you to define board settings in a TOML file and generate the necessary board files for building CircuitPython.

## Overview

The traditional CircuitPython build process requires creating several board-specific files manually in the appropriate port directory. The new board configuration system simplifies this process by:

1. Defining all board settings in a single TOML file
2. Automatically generating the necessary board files
3. Building CircuitPython using these generated files

This approach makes it easier to create custom boards or modify existing ones, especially for users who are not familiar with the internal structure of CircuitPython.

## Prerequisites

Before using the board configuration system, make sure you have:

- Python 3.7 or later
- Required Python packages: `tomli`
- The appropriate toolchain for your target board:
  - ARM GCC for nRF52840 and RP2040 boards
  - ESP-IDF for ESP32 boards

## Getting Started

### 1. Create a Board Configuration File

Start by creating a `board_setting.toml` file for your board. You can use one of the example files in `examples/board_settings/` as a template:

- `nrf52840_example.toml`: Example for nRF52840 boards
- `rp2040_example.toml`: Example for RP2040 boards
- `esp32s3_example.toml`: Example for ESP32-S3 boards

### 2. Set Up the Build Environment

Run the setup script to install dependencies and configure the build environment:

```bash
python3 tools/setup_build_env.py your_board_setting.toml
```

This script will:
- Install required Python packages
- Install the appropriate toolchain if needed
- Fetch necessary submodules
- Build mpy-cross
- Create an environment file with build settings

### 3. Generate Board Files

Generate the board files from your TOML configuration:

```bash
python3 tools/board_config_generator.py your_board_setting.toml
```

This will create the following files in the appropriate port directory:
- `mpconfigboard.h`: Board-specific C header file
- `mpconfigboard.mk`: Board-specific make configuration
- `pins.c`: Pin definitions for the board
- `board.c`: Board initialization code
- Port-specific files (e.g., `sdkconfig` for ESP32)

### 4. Build CircuitPython

Build CircuitPython using the generated board files:

```bash
make build-from-config BOARD_CONFIG=your_board_setting.toml
```

This command will:
1. Generate the board files (if not already done)
2. Build CircuitPython for your board
3. Create firmware files in the appropriate build directory

## Board Configuration File Format

The `board_setting.toml` file is organized into sections that define different aspects of the board.

### Basic Board Information

```toml
[board]
name = "My Custom Board"              # Display name of the board
mcu = "nRF52840"                      # MCU name
port_type = "nordic"                  # Port type: "nordic", "raspberrypi", or "espressif"
directory_name = "my_custom_board"    # Directory name for the board files
chip_variant = "nRF52840"             # Specific chip variant
has_crystal = true                    # Whether the board has an external crystal
```

### USB Configuration

```toml
[usb]
vid = "0x239A"                        # Vendor ID
pid = "0x802A"                        # Product ID
product = "My Custom Board"           # Product name
manufacturer = "My Company"           # Manufacturer name
```

### Flash Memory Configuration

For Nordic boards:
```toml
[flash]
type = "qspi"                         # Flash type: "qspi" or "spi"
devices = ["GD25Q16C", "W25Q16JVxQ"]  # Compatible flash devices
# QSPI pin configuration
data0_port = 0
data0_pin = 17
data1_port = 0
data1_pin = 22
data2_port = 0
data2_pin = 23
data3_port = 0
data3_pin = 21
sck_port = 0
sck_pin = 19
cs_port = 0
cs_pin = 20
```

For Raspberry Pi boards:
```toml
[flash]
devices = ["W25Q16JVxQ"]              # Compatible flash devices
```

For Espressif boards:
```toml
[flash]
size = "8MB"                          # Flash size
mode = "qio"                          # Flash mode: "qio", "dio", "qout", "dout"
freq = "80m"                          # Flash frequency: "80m", "40m", "20m"
```

### PSRAM Configuration (Espressif only)

```toml
[psram]
size = "8MB"                          # PSRAM size
mode = "opi"                          # PSRAM mode: "opi", "spi"
freq = "80m"                          # PSRAM frequency: "80m", "40m"
```

### LED Configuration

```toml
[led]
status = "P1_15"                      # Status LED pin
neopixel = "P0_16"                    # NeoPixel LED pin
neopixel_power = "P1_14"              # NeoPixel power control pin
```

### Default Bus Configurations

```toml
[buses]
[buses.i2c]
scl = "P0_11"                         # I2C SCL pin
sda = "P0_12"                         # I2C SDA pin

[buses.spi]
sck = "P0_14"                         # SPI SCK pin
mosi = "P0_13"                        # SPI MOSI pin
miso = "P0_15"                        # SPI MISO pin

[buses.uart]
rx = "P0_24"                          # UART RX pin
tx = "P0_25"                          # UART TX pin
```

### Pin Definitions

```toml
[pins]
# Pin definitions
A0 = "P0_04"                          # Analog pin A0
A1 = "P0_05"                          # Analog pin A1
D2 = "P0_10"                          # Digital pin D2
D5 = "P1_08"                          # Digital pin D5
# ... more pins
```

### Pin Aliases

```toml
[aliases]
# Pin aliases
LED = "L"                             # LED alias
RED_LED = "L"                         # RED_LED alias
D3 = "L"                              # D3 alias
```

### Board-Specific Features (Raspberry Pi)

```toml
[features]
_EVE = true                           # Enable EVE feature
PICODVI = true                        # Enable PicoDVI feature
```

### SDK Configuration (Espressif)

```toml
[sdkconfig]
"CONFIG_ESP32S3_SPIRAM_SUPPORT" = "y"
"CONFIG_SPIRAM_MODE_OCT" = "y"
"CONFIG_SPIRAM_TYPE_AUTO" = "y"
"CONFIG_SPIRAM_SIZE" = "-1"
"CONFIG_SPIRAM_SPEED_80M" = "y"
"CONFIG_SPIRAM" = "y"
```

### Pico SDK Configuration (Raspberry Pi)

```toml
[pico_sdk_config]
"PICO_BOARD" = "pico"
"PICO_COPY_TO_RAM" = 0
```

## Port-Specific Configuration

### Nordic (nRF52840)

Nordic boards require the following specific configuration:

- `chip_variant`: The specific chip variant (e.g., "nRF52840")
- `flash.type`: Flash memory type ("qspi" or "spi")
- `flash.devices`: List of compatible flash devices
- QSPI pin configuration (for QSPI flash)
- SPI pin configuration (for SPI flash)

### Raspberry Pi (RP2040)

Raspberry Pi boards require the following specific configuration:

- `chip_variant`: The specific chip variant (e.g., "RP2040")
- `chip_family`: The chip family (e.g., "rp2")
- `features`: Board-specific features to enable
- `pico_sdk_config`: Pico SDK configuration options

### Espressif (ESP32-S3)

Espressif boards require the following specific configuration:

- `idf_target`: The target ESP32 variant (e.g., "esp32s3")
- `flash.size`: Flash memory size (e.g., "8MB")
- `flash.mode`: Flash memory mode (e.g., "qio")
- `flash.freq`: Flash memory frequency (e.g., "80m")
- `psram.size`: PSRAM size (e.g., "8MB")
- `psram.mode`: PSRAM mode (e.g., "opi")
- `psram.freq`: PSRAM frequency (e.g., "80m")
- `sdkconfig`: ESP-IDF SDK configuration options

## Examples

### nRF52840 Example

See `examples/board_settings/nrf52840_example.toml` for a complete example based on the Adafruit Feather nRF52840 Express.

### RP2040 Example

See `examples/board_settings/rp2040_example.toml` for a complete example based on the Raspberry Pi Pico.

### ESP32-S3 Example

See `examples/board_settings/esp32s3_example.toml` for a complete example based on the ESP32-S3-DevKitC-1-N8R8.

## Troubleshooting

### Common Issues

1. **Missing dependencies**:
   - Make sure you have installed all required dependencies with `pip install -r requirements-dev.txt`
   - For Espressif boards, make sure ESP-IDF is properly installed and configured

2. **Build errors**:
   - Check that the pin names in your configuration file match the expected format for the port
   - Verify that all required sections are present in your configuration file

3. **Flash errors**:
   - Ensure that the flash configuration matches your board's hardware
   - For Espressif boards, make sure the flash size and mode are correct

### Getting Help

If you encounter issues with the board configuration system, please:

1. Check the CircuitPython documentation
2. Search for similar issues in the CircuitPython GitHub repository
3. Ask for help on the Adafruit Discord server or forums

## Advanced Usage

### Creating a New Board from Scratch

1. Identify the port type for your board (nordic, raspberrypi, espressif)
2. Copy the appropriate example configuration file
3. Update all sections to match your board's specifications
4. Test the configuration by building CircuitPython
5. Iterate as needed to fix any issues

### Modifying an Existing Board

1. Find the board files in the appropriate port directory
2. Create a new configuration file based on the existing board
3. Make your desired changes
4. Build and test the modified configuration

### Contributing Your Board

If you've created a configuration for a new board, consider contributing it back to the CircuitPython project:

1. Add your configuration file to `examples/board_settings/`
2. Submit a pull request with your changes
3. Include documentation about your board in the PR description