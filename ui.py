"""User Interface - Handles menus, prompts, and user interaction"""

import time


# STM32 target configurations
STM32_TARGETS = {
    "1": "target/stm32f0x.cfg",
    "2": "target/stm32f1x.cfg",
    "3": "target/stm32f2x.cfg",
    "4": "target/stm32f3x.cfg",
    "5": "target/stm32f4x.cfg",
    "6": "target/stm32f7x.cfg",
    "7": "target/stm32g0x.cfg",
    "8": "target/stm32g4x.cfg",
    "9": "target/stm32h7x.cfg",
    "10": "target/stm32l0.cfg",
    "11": "target/stm32l1.cfg",
    "12": "target/stm32l4x.cfg",
    "13": "target/stm32l5x.cfg",
    "14": "target/stm32wbx.cfg",
    "15": "target/stm32wlx.cfg"
}


def select_target():
    """Display target selection menu and return selected target config"""
    print("\nSelect STM32 target:")
    print("F Series:")
    print("  1.  STM32F0 (target/stm32f0x.cfg)")
    print("  2.  STM32F1 (target/stm32f1x.cfg)")
    print("  3.  STM32F2 (target/stm32f2x.cfg)")
    print("  4.  STM32F3 (target/stm32f3x.cfg)")
    print("  5.  STM32F4 (target/stm32f4x.cfg)")
    print("  6.  STM32F7 (target/stm32f7x.cfg)")
    print("G Series:")
    print("  7.  STM32G0 (target/stm32g0x.cfg)")
    print("  8.  STM32G4 (target/stm32g4x.cfg)")
    print("H Series:")
    print("  9.  STM32H7 (target/stm32h7x.cfg)")
    print("L Series:")
    print("  10. STM32L0 (target/stm32l0.cfg)")
    print("  11. STM32L1 (target/stm32l1.cfg)")
    print("  12. STM32L4 (target/stm32l4x.cfg)")
    print("  13. STM32L5 (target/stm32l5x.cfg)")
    print("Wireless Series:")
    print("  14. STM32WB (target/stm32wbx.cfg)")
    print("  15. STM32WL (target/stm32wlx.cfg)")

    target_choice = input("\nEnter your choice (1-15): ").strip()

    if target_choice in STM32_TARGETS:
        target_cfg = STM32_TARGETS[target_choice]
        print(f"Selected: {target_cfg}")
        return target_cfg
    else:
        print("Error: Invalid target selection")
        return None


def print_menu():
    """Print interactive menu"""
    print("\n" + "="*50)
    print("OpenOCD Manager - Interactive Menu")
    print("="*50)
    print("1.  Halt MCU")
    print("2.  Reset and Halt MCU")
    print("3.  Reset and Run MCU")
    print("4.  Erase Flash")
    print("5.  Flash Firmware")
    print("6.  Verify Firmware")
    print("7.  Read Memory")
    print("8.  Write Memory")
    print("9.  Get Target Info")
    print("10. Send Custom Command")
    print("11. Reconnect to OpenOCD")
    print("12. Exit")
    print("="*50)


def run_interactive_loop(manager):
    """Run the interactive command loop"""
    try:
        while True:
            print_menu()
            choice = input("\nEnter your choice: ").strip()

            if choice == "1":
                manager.halt()

            elif choice == "2":
                manager.reset_halt()

            elif choice == "3":
                manager.reset_run()

            elif choice == "4":
                confirm = input("Are you sure you want to erase flash? (yes/no): ")
                if confirm.lower() == "yes":
                    manager.erase_flash()

            elif choice == "5":
                firmware_path = input("Enter firmware file path: ").strip()
                manager.flash_firmware(firmware_path)

            elif choice == "6":
                firmware_path = input("Enter firmware file path: ").strip()
                manager.verify_firmware(firmware_path)

            elif choice == "7":
                try:
                    addr_str = input("Enter memory address (hex, e.g., 0x08000000): ").strip()
                    address = int(addr_str, 16) if addr_str.startswith("0x") else int(addr_str, 16)
                    count_str = input("Enter number of words to read (default: 1): ").strip()
                    count = int(count_str) if count_str else 1
                    manager.read_memory(address, count)
                except ValueError:
                    print("Invalid address or count")

            elif choice == "8":
                try:
                    addr_str = input("Enter memory address (hex, e.g., 0x08000000): ").strip()
                    address = int(addr_str, 16) if addr_str.startswith("0x") else int(addr_str, 16)
                    val_str = input("Enter value to write (hex, e.g., 0x12345678): ").strip()
                    value = int(val_str, 16) if val_str.startswith("0x") else int(val_str, 16)
                    manager.write_memory(address, value)
                except ValueError:
                    print("Invalid address or value")

            elif choice == "9":
                manager.get_target_info()

            elif choice == "10":
                command = input("Enter OpenOCD command: ").strip()
                if command:
                    manager.custom_command(command)

            elif choice == "11":
                manager.disconnect()
                time.sleep(1)
                manager.connect_telnet()

            elif choice == "12":
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please try again.")

            input("\nPress Enter to continue...")

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
