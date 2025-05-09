// This file is part of the CircuitPython project: https://circuitpython.org
//
// SPDX-FileCopyrightText: Copyright (c) 2025 CircuitPython Contributors
//
// SPDX-License-Identifier: MIT

#pragma once

#define MICROPY_HW_BOARD_NAME       "Raspberry Pi Pico"
#define MICROPY_HW_MCU_NAME         "RP2040"


#define BOARD_HAS_CRYSTAL 1

#define DEFAULT_I2C_BUS_SCL         (&pin_GP1)
#define DEFAULT_I2C_BUS_SDA         (&pin_GP0)

#define DEFAULT_SPI_BUS_SCK         (&pin_GP18)
#define DEFAULT_SPI_BUS_MOSI        (&pin_GP19)
#define DEFAULT_SPI_BUS_MISO        (&pin_GP16)

#define DEFAULT_UART_BUS_RX         (&pin_GP1)
#define DEFAULT_UART_BUS_TX         (&pin_GP0)

#define CIRCUITPY_BOARD_I2C         (1)
#define CIRCUITPY_BOARD_I2C_PIN     {.scl = &pin_GP1, .sda = &pin_GP0}
