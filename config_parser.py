"""Config File Parser - Parses configuration files for automated operations"""

import os
from colors import error, info, warning


class ConfigParser:
    """Parse and validate configuration files"""

    def __init__(self, config_path):
        self.config_path = config_path
        self.target = None
        self.commands = []

    def parse(self):
        """Parse the configuration file

        Returns:
            tuple: (target_cfg, commands_list) or (None, None) on error
        """
        if not os.path.exists(self.config_path):
            print(error(f"Config file not found: {self.config_path}"))
            return None, None

        try:
            with open(self.config_path, 'r') as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, 1):
                # Strip whitespace and skip empty lines and comments
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # Parse target directive
                if line.lower().startswith('target:'):
                    target_value = line.split(':', 1)[1].strip()
                    self.target = self._parse_target(target_value)
                    if not self.target:
                        print(error(f"Invalid target on line {line_num}: {target_value}"))
                        return None, None

                # Parse command directives
                elif line.lower().startswith('command:'):
                    command_value = line.split(':', 1)[1].strip()
                    cmd = self._parse_command(command_value, line_num)
                    if cmd:
                        self.commands.append(cmd)
                    else:
                        print(error(f"Invalid command on line {line_num}: {command_value}"))
                        return None, None

                else:
                    print(warning(f"Unknown directive on line {line_num}: {line}"))

            # Validate that we have at least a target
            if not self.target:
                print(error("No target specified in config file"))
                return None, None

            if not self.commands:
                print(warning("No commands specified in config file"))

            return self.target, self.commands

        except Exception as e:
            print(error(f"Error reading config file: {e}"))
            return None, None

    def _parse_target(self, target_value):
        """Parse target value and return target config path"""
        # Map of target identifiers to config paths
        target_map = {
            'stm32f0': 'target/stm32f0x.cfg',
            'stm32f1': 'target/stm32f1x.cfg',
            'stm32f2': 'target/stm32f2x.cfg',
            'stm32f3': 'target/stm32f3x.cfg',
            'stm32f4': 'target/stm32f4x.cfg',
            'stm32f7': 'target/stm32f7x.cfg',
            'stm32g0': 'target/stm32g0x.cfg',
            'stm32g4': 'target/stm32g4x.cfg',
            'stm32h7': 'target/stm32h7x.cfg',
            'stm32l0': 'target/stm32l0.cfg',
            'stm32l1': 'target/stm32l1.cfg',
            'stm32l4': 'target/stm32l4x.cfg',
            'stm32l5': 'target/stm32l5x.cfg',
            'stm32wb': 'target/stm32wbx.cfg',
            'stm32wl': 'target/stm32wlx.cfg',
        }

        target_lower = target_value.lower()

        # Check if it's a direct match
        if target_lower in target_map:
            return target_map[target_lower]

        # Check if it's already a path
        if target_value.endswith('.cfg'):
            return target_value

        return None

    def _parse_command(self, command_value, line_num):
        """Parse command and return command dictionary

        Returns:
            dict: Command dictionary with 'type' and optional parameters
        """
        parts = command_value.split()
        if not parts:
            return None

        cmd_type = parts[0].lower()

        # Validate command types
        valid_commands = {
            'halt': {'requires_param': False, 'max_params': 0},
            'reset_halt': {'requires_param': False, 'max_params': 0},
            'reset_run': {'requires_param': False, 'max_params': 0},
            'erase_flash': {'requires_param': False, 'max_params': 0},
            'flash': {'requires_param': True, 'max_params': 2},  # filepath [address]
            'verify': {'requires_param': True, 'max_params': 2},  # filepath [address]
            'read_memory': {'requires_param': True, 'max_params': 2},  # address [count]
            'write_memory': {'requires_param': True, 'max_params': 2},  # address value
            'custom': {'requires_param': True, 'max_params': -1},  # unlimited params
        }

        if cmd_type not in valid_commands:
            return None

        # Get parameters after command type
        cmd_params = parts[1:] if len(parts) > 1 else []

        # Check if parameter is required
        if valid_commands[cmd_type]['requires_param'] and not cmd_params:
            print(error(f"Command '{cmd_type}' requires a parameter (line {line_num})"))
            return None

        # Parse command-specific parameters
        result = {'type': cmd_type}

        if cmd_type in ['flash', 'verify']:
            # flash/verify: filepath [address]
            result['filepath'] = cmd_params[0] if len(cmd_params) > 0 else None
            result['address'] = cmd_params[1] if len(cmd_params) > 1 else None

        elif cmd_type == 'read_memory':
            # read_memory: address [count]
            result['address'] = cmd_params[0] if len(cmd_params) > 0 else None
            result['count'] = cmd_params[1] if len(cmd_params) > 1 else None

        elif cmd_type == 'write_memory':
            # write_memory: address value
            result['address'] = cmd_params[0] if len(cmd_params) > 0 else None
            result['value'] = cmd_params[1] if len(cmd_params) > 1 else None

        elif cmd_type == 'custom':
            # custom: entire rest of line
            result['param'] = ' '.join(cmd_params)

        else:
            # Commands without parameters
            result['param'] = None

        return result
