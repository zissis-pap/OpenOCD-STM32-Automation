"""User Interface - Handles menus, prompts, and user interaction"""

import time
from colors import Colors, header, error, success, info, warning


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
    print(header("\nSelect STM32 target:"))
    print(info("F Series:"))
    print(f"{Colors.CYAN}  1.  STM32F0 {Colors.DIM}(target/stm32f0x.cfg){Colors.RESET}")
    print(f"{Colors.CYAN}  2.  STM32F1 {Colors.DIM}(target/stm32f1x.cfg){Colors.RESET}")
    print(f"{Colors.CYAN}  3.  STM32F2 {Colors.DIM}(target/stm32f2x.cfg){Colors.RESET}")
    print(f"{Colors.CYAN}  4.  STM32F3 {Colors.DIM}(target/stm32f3x.cfg){Colors.RESET}")
    print(f"{Colors.CYAN}  5.  STM32F4 {Colors.DIM}(target/stm32f4x.cfg){Colors.RESET}")
    print(f"{Colors.CYAN}  6.  STM32F7 {Colors.DIM}(target/stm32f7x.cfg){Colors.RESET}")
    print(info("G Series:"))
    print(f"{Colors.CYAN}  7.  STM32G0 {Colors.DIM}(target/stm32g0x.cfg){Colors.RESET}")
    print(f"{Colors.CYAN}  8.  STM32G4 {Colors.DIM}(target/stm32g4x.cfg){Colors.RESET}")
    print(info("H Series:"))
    print(f"{Colors.CYAN}  9.  STM32H7 {Colors.DIM}(target/stm32h7x.cfg){Colors.RESET}")
    print(info("L Series:"))
    print(f"{Colors.CYAN}  10. STM32L0 {Colors.DIM}(target/stm32l0.cfg){Colors.RESET}")
    print(f"{Colors.CYAN}  11. STM32L1 {Colors.DIM}(target/stm32l1.cfg){Colors.RESET}")
    print(f"{Colors.CYAN}  12. STM32L4 {Colors.DIM}(target/stm32l4x.cfg){Colors.RESET}")
    print(f"{Colors.CYAN}  13. STM32L5 {Colors.DIM}(target/stm32l5x.cfg){Colors.RESET}")
    print(info("Wireless Series:"))
    print(f"{Colors.CYAN}  14. STM32WB {Colors.DIM}(target/stm32wbx.cfg){Colors.RESET}")
    print(f"{Colors.CYAN}  15. STM32WL {Colors.DIM}(target/stm32wlx.cfg){Colors.RESET}")

    target_choice = input(f"\n{Colors.PROMPT}Enter your choice (1-15): {Colors.RESET}").strip()

    if target_choice in STM32_TARGETS:
        target_cfg = STM32_TARGETS[target_choice]
        print(success(f"Selected: {target_cfg}"))
        return target_cfg
    else:
        print(error("Error: Invalid target selection"))
        return None


def print_menu():
    """Print interactive menu"""
    print("\n" + header("="*50))
    print(header("OpenOCD Manager - Interactive Menu"))
    print(header("="*50))
    print(f"{Colors.MENU}1.  {Colors.RESET}Halt MCU")
    print(f"{Colors.MENU}2.  {Colors.RESET}Reset and Halt MCU")
    print(f"{Colors.MENU}3.  {Colors.RESET}Reset and Run MCU")
    print(f"{Colors.MENU}4.  {Colors.RESET}Erase Flash")
    print(f"{Colors.MENU}5.  {Colors.RESET}Flash Firmware")
    print(f"{Colors.MENU}6.  {Colors.RESET}Verify Firmware")
    print(f"{Colors.MENU}7.  {Colors.RESET}Read Memory")
    print(f"{Colors.MENU}8.  {Colors.RESET}Write Memory")
    print(f"{Colors.MENU}9.  {Colors.RESET}Get Target Info")
    print(f"{Colors.MENU}10. {Colors.RESET}Send Custom Command")
    print(f"{Colors.MENU}11. {Colors.RESET}Reconnect to OpenOCD")
    print(f"{Colors.MENU}12. {Colors.RESET}Exit")
    print(header("="*50))


def run_interactive_loop(manager):
    """Run the interactive command loop"""
    try:
        while True:
            print_menu()
            choice = input(f"\n{Colors.PROMPT}Enter your choice: {Colors.RESET}").strip()

            if choice == "1":
                manager.halt()

            elif choice == "2":
                manager.reset_halt()

            elif choice == "3":
                manager.reset_run()

            elif choice == "4":
                confirm = input(f"{Colors.WARNING}Are you sure you want to erase flash? (yes/no): {Colors.RESET}")
                if confirm.lower() == "yes":
                    manager.erase_flash()

            elif choice == "5":
                firmware_path = input(f"{Colors.PROMPT}Enter firmware file path: {Colors.RESET}").strip()
                manager.flash_firmware(firmware_path)

            elif choice == "6":
                firmware_path = input(f"{Colors.PROMPT}Enter firmware file path: {Colors.RESET}").strip()
                manager.verify_firmware(firmware_path)

            elif choice == "7":
                try:
                    addr_str = input(f"{Colors.PROMPT}Enter memory address (hex, e.g., 0x08000000): {Colors.RESET}").strip()
                    address = int(addr_str, 16) if addr_str.startswith("0x") else int(addr_str, 16)
                    count_str = input(f"{Colors.PROMPT}Enter number of words to read (default: 1): {Colors.RESET}").strip()
                    count = int(count_str) if count_str else 1
                    manager.read_memory(address, count)
                except ValueError:
                    print(error("Invalid address or count"))

            elif choice == "8":
                try:
                    addr_str = input(f"{Colors.PROMPT}Enter memory address (hex, e.g., 0x08000000): {Colors.RESET}").strip()
                    address = int(addr_str, 16) if addr_str.startswith("0x") else int(addr_str, 16)
                    val_str = input(f"{Colors.PROMPT}Enter value to write (hex, e.g., 0x12345678): {Colors.RESET}").strip()
                    value = int(val_str, 16) if val_str.startswith("0x") else int(val_str, 16)
                    manager.write_memory(address, value)
                except ValueError:
                    print(error("Invalid address or value"))

            elif choice == "9":
                manager.get_target_info()

            elif choice == "10":
                command = input(f"{Colors.PROMPT}Enter OpenOCD command: {Colors.RESET}").strip()
                if command:
                    manager.custom_command(command)

            elif choice == "11":
                manager.disconnect()
                time.sleep(1)
                manager.connect_telnet()

            elif choice == "12":
                print(info("Exiting..."))
                break

            else:
                print(error("Invalid choice. Please try again."))

            input(f"\n{Colors.DIM}Press Enter to continue...{Colors.RESET}")

    except KeyboardInterrupt:
        print(warning("\n\nInterrupted by user"))
