"""Color utilities for terminal output"""

from colorama import Fore, Style, init

# Initialize colorama (auto-reset on Windows)
init(autoreset=True)

# Color definitions
class Colors:
    """Terminal color constants"""
    # Basic colors
    RESET = Style.RESET_ALL
    BRIGHT = Style.BRIGHT
    DIM = Style.DIM

    # Foreground colors
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE

    # Semantic colors for different message types
    SUCCESS = Fore.GREEN
    ERROR = Fore.RED
    WARNING = Fore.YELLOW
    INFO = Fore.CYAN
    HEADER = Fore.CYAN + Style.BRIGHT
    MENU = Fore.BLUE + Style.BRIGHT
    PROMPT = Fore.YELLOW


def colored(text, color):
    """Return colored text

    Args:
        text: The text to color
        color: Color code from Colors class

    Returns:
        Colored text string
    """
    return f"{color}{text}{Colors.RESET}"


def success(text):
    """Return success colored text"""
    return colored(text, Colors.SUCCESS)


def error(text):
    """Return error colored text"""
    return colored(text, Colors.ERROR)


def warning(text):
    """Return warning colored text"""
    return colored(text, Colors.WARNING)


def info(text):
    """Return info colored text"""
    return colored(text, Colors.INFO)


def header(text):
    """Return header colored text"""
    return colored(text, Colors.HEADER)
