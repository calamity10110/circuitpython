#!/usr/bin/env python3

# This file is part of the CircuitPython project: https://circuitpython.org
#
# SPDX-FileCopyrightText: Copyright (c) 2025 CircuitPython Contributors
#
# SPDX-License-Identifier: MIT

"""
This script sets up the build environment for CircuitPython based on a board_setting.toml file.
It installs the necessary dependencies and configures the environment for building.
"""

import argparse
import os
import platform
import subprocess
import sys
from pathlib import Path

import tomli


def run_command(cmd, cwd=None, env=None):
    """Run a command and return its output."""
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(cmd)}")
        print(f"Error: {e.stderr}")
        return None


def setup_environment(config_file):
    """Set up the build environment based on the board configuration."""
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

    # Set up the ARM GCC toolchain path
    gcc_path = "/opt/gcc-arm/arm-gnu-toolchain-13.2.Rel1-x86_64-arm-none-eabi/bin"
    os.environ["PATH"] = f"{gcc_path}:{os.environ.get('PATH', '')}"

    # Create environment variable file
    env_file = "circuitpython_build_process_environment"
    with open(env_file, "w") as f:
        f.write(f"CIRCUITPY_PORT_TYPE={port_type}\n")
        f.write(f"CIRCUITPY_BOARD_CONFIG={os.path.abspath(config_file)}\n")
        f.write(f"PATH={gcc_path}:/tmp/arm-bin:$PATH:/usr/bin\n")

        # Add port-specific environment variables
        if port_type == "nordic":
            f.write(
                "CIRCUITPY_BUILD_TOOLS=arm-none-eabi-gcc arm-none-eabi-g++ arm-none-eabi-ar arm-none-eabi-objcopy arm-none-eabi-size\n"
            )
            f.write(
                "CROSS_COMPILE=/opt/gcc-arm/arm-gnu-toolchain-13.2.Rel1-x86_64-arm-none-eabi/bin/arm-none-eabi-\n"
            )
        elif port_type == "raspberrypi":
            f.write(
                "CIRCUITPY_BUILD_TOOLS=arm-none-eabi-gcc arm-none-eabi-g++ arm-none-eabi-ar arm-none-eabi-objcopy arm-none-eabi-size\n"
            )
            f.write(
                "CROSS_COMPILE=/opt/gcc-arm/arm-gnu-toolchain-13.2.Rel1-x86_64-arm-none-eabi/bin/arm-none-eabi-\n"
            )
        elif port_type == "espressif":
            f.write(
                "CIRCUITPY_BUILD_TOOLS=xtensa-esp32-elf-gcc xtensa-esp32-elf-g++ xtensa-esp32-elf-ar xtensa-esp32-elf-objcopy xtensa-esp32-elf-size\n"
            )

    print(f"Created environment file: {env_file}")

    # Install required dependencies
    print("Installing required dependencies...")

    # Install Python dependencies
    run_command([sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"])

    # Install port-specific dependencies
    if port_type == "nordic":
        setup_nordic_environment()
    elif port_type == "raspberrypi":
        setup_raspberrypi_environment()
    elif port_type == "espressif":
        setup_espressif_environment()

    # Build mpy-cross
    print("Building mpy-cross...")
    run_command(["make", "-C", "mpy-cross"])

    print("Environment setup complete!")
    print(
        f"To build, run: source {env_file} && make build-from-config BOARD_CONFIG={config_file}"
    )

    return True


def setup_nordic_environment():
    """Set up the environment for building Nordic ports."""
    # Use the ARM GCC 13.2 toolchain we installed
    gcc_path = "/opt/gcc-arm/arm-gnu-toolchain-13.2.Rel1-x86_64-arm-none-eabi/bin"

    # Add the toolchain to PATH
    os.environ["PATH"] = f"{gcc_path}:{os.environ.get('PATH', '')}"

    # Create symlinks to ensure tools are found
    print("Creating symlinks for ARM toolchain...")
    run_command(["mkdir", "-p", "/tmp/arm-bin"])
    for tool in ["ar", "objcopy", "size", "gcc", "g++"]:
        run_command(
            [
                "ln",
                "-sf",
                f"{gcc_path}/arm-none-eabi-{tool}",
                f"/tmp/arm-bin/arm-none-eabi-{tool}",
            ]
        )

    # Fetch submodules for Nordic port
    print("Fetching Nordic port submodules...")
    run_command(["make", "fetch-port-submodules"], cwd="ports/nordic")


def setup_raspberrypi_environment():
    """Set up the environment for building Raspberry Pi ports."""
    # Use the ARM GCC 13.2 toolchain we installed
    gcc_path = "/opt/gcc-arm/arm-gnu-toolchain-13.2.Rel1-x86_64-arm-none-eabi/bin"

    # Add the toolchain to PATH
    os.environ["PATH"] = f"{gcc_path}:{os.environ.get('PATH', '')}"

    # Create symlinks to ensure tools are found
    print("Creating symlinks for ARM toolchain...")
    run_command(["mkdir", "-p", "/tmp/arm-bin"])
    for tool in ["ar", "objcopy", "size", "gcc", "g++"]:
        run_command(
            [
                "ln",
                "-sf",
                f"{gcc_path}/arm-none-eabi-{tool}",
                f"/tmp/arm-bin/arm-none-eabi-{tool}",
            ]
        )

    # Fetch submodules for Raspberry Pi port
    print("Fetching Raspberry Pi port submodules...")
    run_command(["make", "fetch-port-submodules"], cwd="ports/raspberrypi")


def setup_espressif_environment():
    """Set up the environment for building Espressif ports."""
    # Check if ESP-IDF is installed
    idf_path = os.environ.get("IDF_PATH")
    if not idf_path:
        print(
            "ESP-IDF not found. Please install ESP-IDF and set IDF_PATH environment variable."
        )
        print(
            "See: https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/"
        )

    # Fetch submodules
    print("Fetching Espressif port submodules...")
    run_command(["make", "fetch-port-submodules"], cwd="ports/espressif")


def main():
    """Parse command line arguments and set up the build environment."""
    parser = argparse.ArgumentParser(
        description="Set up CircuitPython build environment from TOML"
    )
    parser.add_argument("config_file", help="Path to the board_setting.toml file")

    args = parser.parse_args()

    if not os.path.exists(args.config_file):
        print(f"Error: Config file {args.config_file} not found")
        return 1

    success = setup_environment(args.config_file)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
