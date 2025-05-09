# CircuitPython Board Configuration Guide

This guide explains how to use the new board configuration system in CircuitPython. The new system uses a TOML file to define board settings, making it easier to create custom boards or modify existing ones.

## Overview

The board configuration system consists of:

1. A TOML configuration file (`board_setting.toml`) that defines all board-specific settings
2. A Python script (`tools/board_config_generator.py`) that generates the necessary board files
3. A build process that uses these generated files to build CircuitPython

## Getting Started

### Prerequisites

Before using the board configuration system, make sure you have:

- Python 3.7 or later
- Required Python packages: `tomli`
- The appropriate toolchain for your target board (ARM GCC for nRF52840/RP2040, ESP-IDF for ESP32)

### Basic Workflow

1. **Create or modify a board configuration file**:
   - Start with one of the example files in `examples/board_settings/`
   - Modify it to match your board's specifications

2. **Set up the build environment**:
   ```bash
   python3 tools/setup_build_env.py your_board_setting.toml
   ```

3. **Build CircuitPython**:
   ```bash
   make build-from-config BOARD_CONFIG=your_board_setting.toml
   ```

## Board Configuration File Format

The `board_setting.toml` file is organized into sections that define different aspects of the board.

### Basic Board Information

```toml
[board]
name = "My Custom Board"
mcu = "nRF52840"
port_type = "nordic"  # Options: "nordic", "raspberrypi", "espressif"
directory_name = "my_custom_board"
chip_variant = "nRF52840"  # Specific to each port
has_crystal = true  # Whether the board has an external crystal
```

### USB Configuration

```toml
[usb]
vid = "0x239A"  # Vendor ID
pid = "0x802A"  # Product ID
product = "My Custom Board"
manufacturer = "My Company"
```

### Flash Memory Configuration

For Nordic boards:
```toml
[flash]
type = "qspi"  # Options: "qspi", "spi"
devices = ["GD25Q16C", "W25Q16JVxQ"]
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
devices = ["W25Q16JVxQ"]
```

For Espressif boards:
```toml
[flash]
size = "8MB"
mode = "qio"  # Options: "qio", "dio", "qout", "dout"
freq = "80m"  # Options: "80m", "40m", "20m"
```

### PSRAM Configuration (Espressif only)

```toml
[psram]
size = "8MB"
mode = "opi"  # Options: "opi", "spi"
freq = "80m"  # Options: "80m", "40m"
```

### LED Configuration

```toml
[led]
status = "P1_15"  # Status LED pin
neopixel = "P0_16"  # NeoPixel LED pin
neopixel_power = "P1_14"  # NeoPixel power control pin
```

### Default Bus Configurations

```toml
[buses]
[buses.i2c]
scl = "P0_11"
sda = "P0_12"

[buses.spi]
sck = "P0_14"
mosi = "P0_13"
miso = "P0_15"

[buses.uart]
rx = "P0_24"
tx = "P0_25"
```

### Pin Definitions

```toml
[pins]
# Pin definitions
A0 = "P0_04"
A1 = "P0_05"
D2 = "P0_10"
D5 = "P1_08"
# ... more pins
```

### Pin Aliases

```toml
[aliases]
# Pin aliases
LED = "L"
RED_LED = "L"
D3 = "L"
```

### Board-Specific Features (Raspberry Pi)

```toml
[features]
_EVE = true
PICODVI = true
```

### SDK Configuration (Espressif)

```toml
[sdkconfig]
CONFIG_ESP32S3_SPIRAM_SUPPORT=y
CONFIG_SPIRAM_MODE_OCT=y
CONFIG_SPIRAM_TYPE_AUTO=y
CONFIG_SPIRAM_SIZE=-1
CONFIG_SPIRAM_SPEED_80M=y
CONFIG_SPIRAM=y
```

### Pico SDK Configuration (Raspberry Pi)

```toml
[pico_sdk_config]
PICO_BOARD = "pico"
PICO_COPY_TO_RAM = 0
```

## Port-Specific Configuration Options

### Nordic (nRF52840)

- **chip_variant**: The specific chip variant (e.g., "nRF52840")
- **flash.type**: Flash memory type ("qspi" or "spi")
- **flash.devices**: List of compatible flash devices

### Raspberry Pi (RP2040)

- **chip_variant**: The specific chip variant (e.g., "RP2040")
- **chip_family**: The chip family (e.g., "rp2")
- **features**: Board-specific features to enable
- **pico_sdk_config**: Pico SDK configuration options

### Espressif (ESP32-S3)

- **idf_target**: The target ESP32 variant (e.g., "esp32s3")
- **flash.size**: Flash memory size (e.g., "8MB")
- **flash.mode**: Flash memory mode (e.g., "qio")
- **flash.freq**: Flash memory frequency (e.g., "80m")
- **psram.size**: PSRAM size (e.g., "8MB")
- **psram.mode**: PSRAM mode (e.g., "opi")
- **psram.freq**: PSRAM frequency (e.g., "80m")
- **sdkconfig**: ESP-IDF SDK configuration options

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