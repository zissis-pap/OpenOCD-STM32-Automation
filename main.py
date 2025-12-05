#!/usr/bin/env python3
"""
OpenOCD Python Flasher
Main entry point for the application
"""

import sys
from openocd_manager import OpenOCDManager
from ui import select_target, run_interactive_loop

VERSION = "0.003"


def main():
    """Main application entry point"""
    print(f"OpenOCD Manager v{VERSION}")
    print("="*50)

    # Hardcoded interface configuration
    interface_cfg = "interface/stlink.cfg"
    port = 4444

    # Ask user to select target
    target_cfg = select_target()
    if not target_cfg:
        return 1

    # Initialize manager
    manager = OpenOCDManager(interface_cfg=interface_cfg, target_cfg=target_cfg, port=port)

    # Start OpenOCD
    if not manager.start_openocd():
        print("Failed to start OpenOCD. Exiting...")
        return 1

    # Connect via telnet
    if not manager.connect_telnet():
        print("Failed to connect to OpenOCD. Stopping...")
        manager.stop_openocd()
        return 1

    # Run interactive loop
    try:
        run_interactive_loop(manager)
    finally:
        print("\nCleaning up...")
        manager.stop_openocd()
        print("Goodbye!")

    return 0


if __name__ == "__main__":
    sys.exit(main())
