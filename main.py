#!/usr/bin/env python3
"""
OpenOCD Python Flasher
Main entry point for the application
"""

import sys
from openocd_manager import OpenOCDManager
from ui import select_target, run_interactive_loop
from colors import header, error, success

VERSION = "0.005"


def main():
    """Main application entry point"""
    print(header(f"OpenOCD Manager v{VERSION}"))
    print(header("="*50))

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
        print(error("Failed to start OpenOCD. Exiting..."))
        return 1

    # Connect via telnet
    if not manager.connect_telnet():
        print(error("Failed to connect to OpenOCD. Stopping..."))
        manager.stop_openocd()
        return 1

    # Run interactive loop
    try:
        run_interactive_loop(manager)
    finally:
        print(header("\nCleaning up..."))
        manager.stop_openocd()
        print(success("Goodbye!"))

    return 0


if __name__ == "__main__":
    sys.exit(main())
