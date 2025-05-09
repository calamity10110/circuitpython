// This file is part of the CircuitPython project: https://circuitpython.org
//
// SPDX-FileCopyrightText: Copyright (c) 2025 CircuitPython Contributors
//
// SPDX-License-Identifier: MIT

#pragma once

#include "nrfx/hal/nrf_gpio.h"

#define MICROPY_HW_BOARD_NAME       "Feather nRF52840"
#define MICROPY_HW_MCU_NAME         "nRF52840"

#define MICROPY_HW_LED_STATUS       (&pin_LED1)
#define MICROPY_HW_NEOPIXEL         (&pin_NEOPIXEL)
#define CIRCUITPY_STATUS_LED_POWER (&pin_NEOPIXEL_POWER)

#if QSPI_FLASH_FILESYSTEM
#define MICROPY_QSPI_DATA0                NRF_GPIO_PIN_MAP(0, 17)
#define MICROPY_QSPI_DATA1                NRF_GPIO_PIN_MAP(0, 22)
#define MICROPY_QSPI_DATA2                NRF_GPIO_PIN_MAP(0, 23)
#define MICROPY_QSPI_DATA3                NRF_GPIO_PIN_MAP(0, 21)
#define MICROPY_QSPI_SCK                  NRF_GPIO_PIN_MAP(0, 19)
#define MICROPY_QSPI_CS                   NRF_GPIO_PIN_MAP(0, 20)
#endif

#define BOARD_HAS_CRYSTAL 1

#define DEFAULT_I2C_BUS_SCL         (&pin_SCL)
#define DEFAULT_I2C_BUS_SDA         (&pin_SDA)

#define DEFAULT_SPI_BUS_SCK         (&pin_SCK)
#define DEFAULT_SPI_BUS_MOSI        (&pin_MOSI)
#define DEFAULT_SPI_BUS_MISO        (&pin_MISO)

#define DEFAULT_UART_BUS_RX         (&pin_RX)
#define DEFAULT_UART_BUS_TX         (&pin_TX)
