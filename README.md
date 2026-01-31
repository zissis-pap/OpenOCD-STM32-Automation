# OpenOCD-STM32-Automation 🔧

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-0.008-green.svg)](https://github.com/yourusername/OpenOCD-STM32-Automation)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey.svg)](https://github.com/yourusername/OpenOCD-STM32-Automation)

A modular Python application for managing OpenOCD connections and performing common embedded development operations on STM32 microcontrollers. Supports both interactive mode and automated scripting via configuration files.

## Table of Contents 📑

- [Features](#features)
- [Supported Devices](#supported-devices)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Interactive Mode](#interactive-mode)
  - [Automated Mode](#automated-mode-configuration-file)
- [Example Workflows](#example-workflows)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features ✨

- **Two operation modes:**
  - **Interactive mode:** Menu-driven interface for manual operations
  - **Automated mode:** Configuration file support for scripted workflows
- Modular, maintainable architecture
- Automatic OpenOCD process management
- Telnet connection to OpenOCD
- Support for 15 STM32 MCU families
- **Robust error handling:**
  - Automatic command retry with halt checking (up to 3 attempts)
  - File existence validation before flash/verify operations
  - Proper exception handling with clear error messages
  - Automatic flash erase on failure in automated mode to prevent bricked devices
- **Color-coded terminal output for better readability:**
  - Green for success messages
  - Red for errors
  - Yellow for warnings and prompts
  - Cyan for information
  - Blue for menu options
- **Common operations:**
  - Halt/Reset MCU
  - Erase flash memory
  - Flash firmware
  - Verify firmware
  - Read/Write memory locations
  - Send custom OpenOCD commands

## Supported Devices 🎯

This tool supports **15 STM32 microcontroller families** across multiple series:

**F Series (Performance):**
- STM32F0, F1, F2, F3, F4, F7

**G Series (Mainstream):**
- STM32G0, G4

**H Series (High Performance):**
- STM32H7

**L Series (Ultra Low Power):**
- STM32L0, L1, L4, L5

**Wireless Series:**
- STM32WB (Bluetooth/802.15.4), WL (LoRa/Sub-GHz)

## Requirements 📋

- Python 3.6+
- OpenOCD installed and in PATH
- Python package: `colorama` (for colored terminal output)
- Target hardware connected via debug probe (ST-Link, J-Link, etc.)

## Installation 💿

1. Install OpenOCD:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install openocd

   # macOS
   brew install openocd

   # Windows
   # Download from https://openocd.org/
   ```

2. Clone or download all project files:
   - `main.py`
   - `openocd_manager.py`
   - `ui.py`
   - `colors.py`
   - `config_parser.py`
   - `requirements.txt`
   - `example_config.txt` (optional example)

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install colorama
   ```

4. Ensure all files are in the same directory

5. Make the main script executable (Linux/macOS):
   ```bash
   chmod +x main.py
   ```

## Configuration ⚙️

The script is pre-configured for **ST-Link debug probe** and supports 15 STM32 target families.

No additional configuration files are needed. Simply select your target when prompted during script startup. 🎯

## Usage 🚀

The application supports two modes of operation:

### 🖥️ Interactive Mode

Run the script without arguments for interactive mode:
```bash
python3 main.py
```

Or:
```bash
./main.py
```

You'll be prompted to select your STM32 target from 15 supported families:
```
Select STM32 target:
F Series:
  1.  STM32F0 (target/stm32f0x.cfg)
  2.  STM32F1 (target/stm32f1x.cfg)
  ...
  (15 options total)

Enter your choice (1-15):
```

After selecting your target, you'll see an interactive menu with the following options:

1. **Halt MCU** - Stop the microcontroller
2. **Reset and Halt MCU** - Reset and immediately halt
3. **Reset and Run MCU** - Reset and let it run
4. **Erase Flash** - Erase the flash memory
5. **Flash Firmware** - Program firmware to the device
6. **Verify Firmware** - Verify programmed firmware
7. **Read Memory** - Read from memory address
8. **Write Memory** - Write to memory address
9. **Get Target Info** - Display target information
10. **Send Custom Command** - Send any OpenOCD command
11. **Reconnect to OpenOCD** - Reconnect telnet session
12. **Exit** - Clean up and exit

### ⚙️ Automated Mode (Configuration File)

For scripted/automated operations, you can use a configuration file:

```bash
python3 main.py config.txt
```

The configuration file uses a simple text format with two types of directives:

#### Target Directive (Required)
```
target: stm32f4
```

Supported target values: `stm32f0`, `stm32f1`, `stm32f2`, `stm32f3`, `stm32f4`, `stm32f7`, `stm32g0`, `stm32g4`, `stm32h7`, `stm32l0`, `stm32l1`, `stm32l4`, `stm32l5`, `stm32wb`, `stm32wl`

#### Command Directives (Optional)
Commands are executed sequentially in the order they appear:

```
command: halt
command: erase_flash
command: flash firmware.bin
command: verify firmware.bin
command: reset_run
```

**Available commands:**
- `halt` - Halt the MCU
- `reset_halt` - Reset and halt the MCU
- `reset_run` - Reset and run the MCU
- `erase_flash` - Erase flash memory
- `flash <filepath> [address]` - Flash firmware, optionally at a specific address
  - Example: `flash build/firmware.bin`
  - Example: `flash build/firmware.bin 0x08004000` (flash at bootloader offset)
- `verify <filepath> [address]` - Verify firmware, optionally at a specific address
  - Example: `verify build/firmware.bin`
  - Example: `verify build/firmware.bin 0x08004000`
- `read_memory <address> [count]` - Read memory (e.g., `read_memory 0x08000000 16`)
- `write_memory <address> <value>` - Write memory (e.g., `write_memory 0x20000000 0x12345678`)
- `custom <command>` - Send custom OpenOCD command (e.g., `custom targets`)

**Example Configuration File:**
```
# Flash and verify firmware on STM32F4
target: stm32f4

# Prepare MCU
command: halt
command: erase_flash

# Program and verify
command: flash firmware.bin
command: verify firmware.bin

# Start execution
command: reset_run
```

Comments (lines starting with `#`) and blank lines are ignored. See `example_config.txt` for a complete example.

### Automatic Halt Check and Retry Logic

The script provides robust error handling for operations that require the MCU to be halted:

**Pre-command Halt Check:**
- Before executing flash operations, memory writes, or verification, the script checks if the MCU is halted
- If not halted, it displays: `MCU not halted, attempting to halt...` and halts it automatically
- This prevents common errors like `"Target not halted\nfailed erasing sectors 0 to 127"`

**Automatic Retry Logic:**
- If a command fails, it automatically retries up to 3 times
- Displays: `Command failed, retrying (2/3)...`
- Before each retry, the script checks if the MCU is halted and halts it if needed
- Detects OpenOCD failure patterns like "failed", "error", "target not halted", "unable to", etc.
- This improves reliability when working with unstable connections or busy targets

**Automated Mode Error Handling:**
- When a command fails in automated mode (config file), the script:
1. Skips all remaining commands in the sequence
2. Performs a flash erase to ensure the device is in a clean state
3. Displays "Task Failed" to clearly indicate the failure
4. Exits with return code 1 for CI/CD integration
- This safety mechanism prevents partially-programmed devices that could fail to boot

**File Validation:**
- Flash and verify operations now include automatic file existence checking
- If a firmware file is not found, the operation immediately fails with a clear error message
- Proper exception handling (`FileNotFoundError`) ensures errors are caught early before attempting communication with the device
- Helps prevent wasted time on operations that cannot succeed due to missing files

## Example Workflows 💡

### 📲 Interactive Mode: Flashing Firmware

1. Start the script: `python3 main.py`
2. Select target: Enter `1-15` based on your STM32 family (e.g., `5` for STM32F4, `10` for STM32L0)
3. Select option `4` to erase flash
4. Select option `5` to flash firmware
5. Enter firmware path: `build/firmware.bin`
6. Select option `6` to verify
7. Select option `3` to reset and run

### 📖 Interactive Mode: Reading Memory

1. Select option `7` (Read Memory)
2. Enter address: `0x08000000` (flash start on STM32)
3. Enter count: `16` (read 16 words)

### ✍️ Interactive Mode: Writing to Memory

1. Select option `8` (Write Memory)
2. Enter address: `0x20000000` (RAM address)
3. Enter value: `0x12345678`

### 🤖 Automated Mode: Complete Flash Workflow

1. Create a configuration file `flash_config.txt`:
```
target: stm32l4
command: halt
command: erase_flash
command: flash build/firmware.bin
command: verify build/firmware.bin
command: reset_run
```

2. Run with config file:
```bash
python3 main.py flash_config.txt
```

The script will automatically execute all commands and report the results.

### 🔀 Automated Mode: Bootloader + Application Flash

For systems with bootloader and application firmware at different addresses:

```
target: stm32f4

# Flash bootloader at base address
command: halt
command: erase_flash
command: flash bootloader.bin 0x08000000
command: verify bootloader.bin 0x08000000

# Flash application at offset
command: flash application.bin 0x08004000
command: verify application.bin 0x08004000

command: reset_run
```

This allows you to program firmware at specific memory locations, useful for:
- Bootloader + application partitioning
- Multi-region firmware updates
- Factory programming scenarios

### 🔄 Automated Mode: CI/CD Integration

Use configuration files in your build pipeline for automated testing:

```bash
# Build firmware
make build

# Flash and verify using config file
python3 main.py deploy_config.txt

# Check exit code
if [ $? -eq 0 ]; then
    echo "Deployment successful"
else
    echo "Deployment failed"
    exit 1
fi
```

## Troubleshooting 🔍

### ❌ OpenOCD fails to start

- Check that OpenOCD is installed: `openocd --version`
- Ensure your ST-Link debug probe is connected
- Verify you selected the correct target for your MCU

### 🔌 Cannot connect via telnet

- Check that OpenOCD started successfully
- Verify the telnet port (default: 4444)
- Try connecting manually: `telnet localhost 4444`

### ⚠️ Flash/Programming errors

- Ensure the MCU is halted before flashing (the script will attempt this automatically)
- Check that the firmware file path is correct - the script will now report "Firmware file 'filename' not found" if the file doesn't exist
- Verify the firmware is compatible with your target
- Ensure the file path is correct relative to where you're running the script from

## Project Structure 📁

```
.
├── main.py              # Entry point and main application logic
├── openocd_manager.py   # OpenOCD process and communication management
├── ui.py                # User interface (menus, prompts, interactive loop)
├── colors.py            # Color utilities for terminal output
├── config_parser.py     # Configuration file parser
├── requirements.txt     # Python dependencies
├── example_config.txt   # Example configuration file
└── LICENSE              # GPL-3.0 license file
```

## Contributing 🤝

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Test thoroughly** with your target hardware
5. **Commit your changes** (`git commit -m 'Add some amazing feature'`)
6. **Push to the branch** (`git push origin feature/amazing-feature`)
7. **Open a Pull Request**

Please ensure your code follows the existing style and includes appropriate error handling.

## License 📄

This project is licensed under the **GNU General Public License v3.0** - see the [LICENSE](LICENSE) file for details.

Copyright (C) 2026 - Zissis Papadopoulos

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

## Acknowledgments 🙏

- Thanks to the [OpenOCD](https://openocd.org/) project for providing the excellent debugging and programming tool
- STMicroelectronics for their comprehensive STM32 microcontroller family

