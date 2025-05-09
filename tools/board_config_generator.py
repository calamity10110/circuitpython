#!/usr/bin/env python3

# This file is part of the CircuitPython project: https://circuitpython.org
#
# SPDX-FileCopyrightText: Copyright (c) 2025 CircuitPython Contributors
#
# SPDX-License-Identifier: MIT

"""
This script generates board configuration files from a board_setting.toml file.
It creates the necessary files for building CircuitPython for a specific board.
"""

import argparse
import os
import sys
from datetime import datetime

import tomli


def generate_header():
    """Generate the standard header for CircuitPython files."""
    year = datetime.now().year
    return f"""// This file is part of the CircuitPython project: https://circuitpython.org
//
// SPDX-FileCopyrightText: Copyright (c) {year} CircuitPython Contributors
//
// SPDX-License-Identifier: MIT

"""


def generate_mpconfigboard_h(config, port_type):
    """Generate the mpconfigboard.h file based on the board configuration."""
    content = generate_header()
    content += "#pragma once\n\n"

    # Add port-specific includes
    if port_type == "nordic":
        content += '#include "nrfx/hal/nrf_gpio.h"\n\n'

    # Board and MCU names
    content += f"#define MICROPY_HW_BOARD_NAME       \"{config['board']['name']}\"\n"
    content += f"#define MICROPY_HW_MCU_NAME         \"{config['board']['mcu']}\"\n\n"

    # Add LED definitions
    if "led" in config:
        if "status" in config["led"]:
            content += f"#define MICROPY_HW_LED_STATUS       (&pin_{config['led']['status']})\n"
        if "neopixel" in config["led"]:
            content += f"#define MICROPY_HW_NEOPIXEL         (&pin_{config['led']['neopixel']})\n"
        if "neopixel_power" in config["led"]:
            content += f"#define CIRCUITPY_STATUS_LED_POWER (&pin_{config['led']['neopixel_power']})\n"

    # Add flash configuration for Nordic
    if port_type == "nordic" and "flash" in config:
        if config["flash"].get("type") == "qspi":
            content += "\n#if QSPI_FLASH_FILESYSTEM\n"
            content += f"#define MICROPY_QSPI_DATA0                NRF_GPIO_PIN_MAP({config['flash']['data0_port']}, {config['flash']['data0_pin']})\n"
            content += f"#define MICROPY_QSPI_DATA1                NRF_GPIO_PIN_MAP({config['flash']['data1_port']}, {config['flash']['data1_pin']})\n"
            content += f"#define MICROPY_QSPI_DATA2                NRF_GPIO_PIN_MAP({config['flash']['data2_port']}, {config['flash']['data2_pin']})\n"
            content += f"#define MICROPY_QSPI_DATA3                NRF_GPIO_PIN_MAP({config['flash']['data3_port']}, {config['flash']['data3_pin']})\n"
            content += f"#define MICROPY_QSPI_SCK                  NRF_GPIO_PIN_MAP({config['flash']['sck_port']}, {config['flash']['sck_pin']})\n"
            content += f"#define MICROPY_QSPI_CS                   NRF_GPIO_PIN_MAP({config['flash']['cs_port']}, {config['flash']['cs_pin']})\n"
            content += "#endif\n"
        elif config["flash"].get("type") == "spi":
            content += "\n#if SPI_FLASH_FILESYSTEM\n"
            content += f"#define SPI_FLASH_MOSI_PIN &pin_{config['flash']['mosi']}\n"
            content += f"#define SPI_FLASH_MISO_PIN &pin_{config['flash']['miso']}\n"
            content += f"#define SPI_FLASH_SCK_PIN &pin_{config['flash']['sck']}\n"
            content += f"#define SPI_FLASH_CS_PIN &pin_{config['flash']['cs']}\n"
            content += "#endif\n"

    # Add crystal configuration
    if "board" in config and "has_crystal" in config["board"]:
        content += f"\n#define BOARD_HAS_CRYSTAL {1 if config['board']['has_crystal'] else 0}\n"

    # Add default bus configurations
    if "buses" in config:
        content += "\n"
        if "i2c" in config["buses"]:
            content += f"#define DEFAULT_I2C_BUS_SCL         (&pin_{config['buses']['i2c']['scl']})\n"
            content += f"#define DEFAULT_I2C_BUS_SDA         (&pin_{config['buses']['i2c']['sda']})\n\n"

        if "spi" in config["buses"]:
            content += f"#define DEFAULT_SPI_BUS_SCK         (&pin_{config['buses']['spi']['sck']})\n"
            content += f"#define DEFAULT_SPI_BUS_MOSI        (&pin_{config['buses']['spi']['mosi']})\n"
            content += f"#define DEFAULT_SPI_BUS_MISO        (&pin_{config['buses']['spi']['miso']})\n\n"

        if "uart" in config["buses"]:
            content += f"#define DEFAULT_UART_BUS_RX         (&pin_{config['buses']['uart']['rx']})\n"
            content += f"#define DEFAULT_UART_BUS_TX         (&pin_{config['buses']['uart']['tx']})\n"

    # Add board-specific I2C configuration for Raspberry Pi
    if port_type == "raspberrypi" and "buses" in config and "i2c" in config["buses"]:
        content += "\n#define CIRCUITPY_BOARD_I2C         (1)\n"
        content += f"#define CIRCUITPY_BOARD_I2C_PIN     {{.scl = &pin_{config['buses']['i2c']['scl']}, .sda = &pin_{config['buses']['i2c']['sda']}}}\n"

    return content


def generate_mpconfigboard_mk(config, port_type):
    """Generate the mpconfigboard.mk file based on the board configuration."""
    content = ""

    # USB configuration
    if "usb" in config:
        content += f"USB_VID = {config['usb']['vid']}\n"
        content += f"USB_PID = {config['usb']['pid']}\n"
        content += f"USB_PRODUCT = \"{config['usb']['product']}\"\n"
        content += f"USB_MANUFACTURER = \"{config['usb']['manufacturer']}\"\n\n"

    # MCU configuration
    if port_type == "nordic":
        content += f"MCU_CHIP = {config['board']['chip_variant'].lower()}\n\n"

        # Flash configuration
        if "flash" in config:
            if config["flash"].get("type") == "qspi":
                content += "QSPI_FLASH_FILESYSTEM = 1\n"
            elif config["flash"].get("type") == "spi":
                content += "SPI_FLASH_FILESYSTEM = 1\n"

            if "devices" in config["flash"]:
                content += f"EXTERNAL_FLASH_DEVICES = \"{', '.join(config['flash']['devices'])}\"\n"

    elif port_type == "raspberrypi":
        content += f"CHIP_VARIANT = {config['board']['chip_variant']}\n"
        content += f"CHIP_FAMILY = {config['board']['chip_family']}\n\n"

        if "flash" in config and "devices" in config["flash"]:
            content += f"EXTERNAL_FLASH_DEVICES = \"{', '.join(config['flash']['devices'])}\"\n\n"

        # Add Raspberry Pi specific features
        if "features" in config:
            for feature, value in config["features"].items():
                if value:
                    content += f"CIRCUITPY_{feature.upper()} = 1\n"

    elif port_type == "espressif":
        content += f"IDF_TARGET = {config['board']['idf_target']}\n\n"

        # Flash configuration
        if "flash" in config:
            if "size" in config["flash"]:
                content += f"CIRCUITPY_ESP_FLASH_SIZE = {config['flash']['size']}\n"
            if "mode" in config["flash"]:
                content += f"CIRCUITPY_ESP_FLASH_MODE = {config['flash']['mode']}\n"
            if "freq" in config["flash"]:
                content += f"CIRCUITPY_ESP_FLASH_FREQ = {config['flash']['freq']}\n"

        # PSRAM configuration
        if "psram" in config:
            content += "\n"
            if "size" in config["psram"]:
                content += f"CIRCUITPY_ESP_PSRAM_SIZE = {config['psram']['size']}\n"
            if "mode" in config["psram"]:
                content += f"CIRCUITPY_ESP_PSRAM_MODE = {config['psram']['mode']}\n"
            if "freq" in config["psram"]:
                content += f"CIRCUITPY_ESP_PSRAM_FREQ = {config['psram']['freq']}\n"

    return content


def generate_pins_c(config, port_type):
    """Generate the pins.c file based on the board configuration."""
    content = generate_header()
    content += '#include "shared-bindings/board/__init__.h"\n\n'
    content += "static const mp_rom_map_elem_t board_module_globals_table[] = {\n"
    content += "    CIRCUITPYTHON_BOARD_DICT_STANDARD_ITEMS\n\n"

    # Add pin definitions
    if "pins" in config:
        for pin_name, pin_value in config["pins"].items():
            content += f"    {{ MP_ROM_QSTR(MP_QSTR_{pin_name}), MP_ROM_PTR(&pin_{pin_value}) }},\n"

    # Add aliases
    if "aliases" in config:
        for alias_name, alias_target in config["aliases"].items():
            content += f"    {{ MP_ROM_QSTR(MP_QSTR_{alias_name}), MP_ROM_PTR(&pin_{config['pins'][alias_target]}) }},\n"

    # Add standard bus objects
    content += "\n    { MP_ROM_QSTR(MP_QSTR_UART), MP_ROM_PTR(&board_uart_obj) },\n"
    content += "    { MP_ROM_QSTR(MP_QSTR_SPI), MP_ROM_PTR(&board_spi_obj) },\n"
    content += "    { MP_ROM_QSTR(MP_QSTR_I2C), MP_ROM_PTR(&board_i2c_obj) },\n"

    content += "};\n\n"
    content += (
        "MP_DEFINE_CONST_DICT(board_module_globals, board_module_globals_table);\n"
    )

    return content


def generate_board_c(config):
    """Generate the board.c file with initialization functions."""
    content = generate_header()
    content += '#include "supervisor/board.h"\n'
    content += '#include "mpconfigboard.h"\n\n'
    content += "void board_init(void) {\n"
    content += "}\n\n"
    content += "bool board_requests_safe_mode(void) {\n"
    content += "    return false;\n"
    content += "}\n\n"
    content += "void reset_board(void) {\n"
    content += "}\n"

    return content


def generate_sdkconfig(config):
    """Generate the sdkconfig file for ESP32."""
    content = ""
    if "sdkconfig" in config:
        for key, value in config["sdkconfig"].items():
            content += f"{key}={value}\n"
    return content


def generate_pico_sdk_configboard_h(config):
    """Generate the pico-sdk-configboard.h file for Raspberry Pi Pico."""
    content = generate_header()
    content += "#pragma once\n\n"

    if "pico_sdk_config" in config:
        for key, value in config["pico_sdk_config"].items():
            content += f"#define {key} {value}\n"

    return content


def create_board_files(config_file, output_dir=None):
    """Parse the TOML configuration file and generate board files."""
    try:
        with open(config_file, "rb") as f:
            config = tomli.load(f)
    except Exception as e:
        print(f"Error loading TOML file: {e}")
        return False

    # Determine port type
    port_type = config.get("board", {}).get("port_type", "").lower()
    if not port_type:
        print("Error: port_type not specified in the configuration file")
        return False

    if port_type not in ["nordic", "raspberrypi", "espressif"]:
        print(f"Error: Unsupported port type: {port_type}")
        return False

    # Create output directory if not specified
    if output_dir is None:
        board_name = config.get("board", {}).get("directory_name", "").lower()
        if not board_name:
            print("Error: board directory_name not specified in the configuration file")
            return False

        output_dir = os.path.join("ports", port_type, "boards", board_name)

    os.makedirs(output_dir, exist_ok=True)

    # Generate files
    files_to_generate = {
        "mpconfigboard.h": generate_mpconfigboard_h(config, port_type),
        "mpconfigboard.mk": generate_mpconfigboard_mk(config, port_type),
        "pins.c": generate_pins_c(config, port_type),
        "board.c": generate_board_c(config),
    }

    # Add port-specific files
    if port_type == "espressif":
        files_to_generate["sdkconfig"] = generate_sdkconfig(config)
    elif port_type == "raspberrypi":
        files_to_generate["pico-sdk-configboard.h"] = generate_pico_sdk_configboard_h(
            config
        )

    # Write files
    for filename, content in files_to_generate.items():
        file_path = os.path.join(output_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Generated {file_path}")

    return True


def main():
    """Parse command line arguments and generate board configuration files."""
    parser = argparse.ArgumentParser(
        description="Generate CircuitPython board configuration files from TOML"
    )
    parser.add_argument("config_file", help="Path to the board_setting.toml file")
    parser.add_argument("--output-dir", help="Output directory for the generated files")

    args = parser.parse_args()

    if not os.path.exists(args.config_file):
        print(f"Error: Config file {args.config_file} not found")
        return 1

    success = create_board_files(args.config_file, args.output_dir)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
