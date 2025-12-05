"""OpenOCD Manager - Handles OpenOCD process and communication"""

import subprocess
import socket
import time
import os


class OpenOCDManager:
    def __init__(self, interface_cfg=None, target_cfg=None, port=4444):
        self.interface_cfg = interface_cfg
        self.target_cfg = target_cfg
        self.port = port
        self.process = None
        self.socket = None
        self.connected = False
        self.buffer = b""

    def start_openocd(self):
        """Start OpenOCD process"""
        if self.process and self.process.poll() is None:
            print("OpenOCD is already running")
            return True

        cmd = ["openocd"]
        if self.interface_cfg:
            cmd.extend(["-f", self.interface_cfg])
        if self.target_cfg:
            cmd.extend(["-f", self.target_cfg])

        try:
            print(f"Starting OpenOCD with command: {' '.join(cmd)}")
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            time.sleep(2)  # Give OpenOCD time to start

            if self.process.poll() is not None:
                _, stderr = self.process.communicate()
                print(f"OpenOCD failed to start: {stderr}")
                return False

            print("OpenOCD started successfully")
            return True
        except FileNotFoundError:
            print("Error: openocd command not found. Please install OpenOCD.")
            return False
        except Exception as e:
            print(f"Error starting OpenOCD: {e}")
            return False

    def connect_telnet(self):
        """Connect to OpenOCD via telnet"""
        if self.connected:
            print("Already connected to OpenOCD")
            return True

        try:
            print(f"Connecting to OpenOCD on localhost:{self.port}...")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)
            self.socket.connect(("localhost", self.port))

            # Read initial prompt
            self._read_until(b">", timeout=2)
            self.connected = True
            print("Connected to OpenOCD successfully")
            return True
        except Exception as e:
            print(f"Error connecting to OpenOCD: {e}")
            self.connected = False
            if self.socket:
                self.socket.close()
                self.socket = None
            return False

    def _read_until(self, delimiter, timeout=5):
        """Read from socket until delimiter is found"""
        self.socket.settimeout(timeout)
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                data = self.socket.recv(4096)
                if not data:
                    break
                self.buffer += data
                if delimiter in self.buffer:
                    result, self.buffer = self.buffer.split(delimiter, 1)
                    return result + delimiter
            except socket.timeout:
                break
            except Exception:
                break

        result = self.buffer
        self.buffer = b""
        return result

    def send_command(self, command):
        """Send command to OpenOCD and return response"""
        if not self.connected:
            print("Not connected to OpenOCD")
            return None

        try:
            self.socket.sendall(f"{command}\n".encode('ascii'))
            response = self._read_until(b">", timeout=5).decode('ascii')
            # Remove the prompt from response
            response = response.rsplit('>', 1)[0].strip()
            return response
        except Exception as e:
            print(f"Error sending command: {e}")
            return None

    def halt(self):
        """Halt the MCU"""
        print("Halting MCU...")
        response = self.send_command("halt")
        if response:
            print(response)
        return response

    def reset_halt(self):
        """Reset and halt the MCU"""
        print("Resetting and halting MCU...")
        response = self.send_command("reset halt")
        if response:
            print(response)
        return response

    def reset_run(self):
        """Reset and run the MCU"""
        print("Resetting and running MCU...")
        response = self.send_command("reset run")
        if response:
            print(response)
        return response

    def erase_flash(self):
        """Erase flash memory"""
        print("Erasing flash memory...")
        response = self.send_command("flash erase_sector 0 0 last")
        if response:
            print(response)
        return response

    def flash_firmware(self, firmware_path):
        """Flash firmware to MCU"""
        if not os.path.exists(firmware_path):
            print(f"Error: Firmware file '{firmware_path}' not found")
            return None

        print(f"Flashing firmware: {firmware_path}")
        self.halt()
        response = self.send_command(f"program {firmware_path} verify reset")
        if response:
            print(response)
        return response

    def verify_firmware(self, firmware_path):
        """Verify firmware"""
        if not os.path.exists(firmware_path):
            print(f"Error: Firmware file '{firmware_path}' not found")
            return None

        print(f"Verifying firmware: {firmware_path}")
        response = self.send_command(f"verify_image {firmware_path}")
        if response:
            print(response)
        return response

    def read_memory(self, address, count=1):
        """Read memory at address"""
        print(f"Reading memory at 0x{address:08x} (count: {count})...")
        response = self.send_command(f"mdw 0x{address:08x} {count}")
        if response:
            print(response)
        return response

    def write_memory(self, address, value):
        """Write value to memory address"""
        print(f"Writing 0x{value:08x} to address 0x{address:08x}...")
        response = self.send_command(f"mww 0x{address:08x} 0x{value:08x}")
        if response:
            print(response)
        return response

    def get_target_info(self):
        """Get target information"""
        print("Getting target information...")
        response = self.send_command("targets")
        if response:
            print(response)
        return response

    def custom_command(self, command):
        """Send custom OpenOCD command"""
        print(f"Sending command: {command}")
        response = self.send_command(command)
        if response:
            print(response)
        return response

    def disconnect(self):
        """Disconnect socket connection"""
        if self.socket:
            try:
                self.socket.close()
                print("Disconnected from OpenOCD")
            except:
                pass
            self.connected = False
            self.socket = None
            self.buffer = b""

    def stop_openocd(self):
        """Stop OpenOCD process"""
        self.disconnect()

        if self.process and self.process.poll() is None:
            print("Stopping OpenOCD...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            print("OpenOCD stopped")
        self.process = None
