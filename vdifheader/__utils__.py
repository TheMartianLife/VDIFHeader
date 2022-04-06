import sys

__GREEN = '\033[0;32m'
__RED = '\033[0;31m'
__YELLOW = '\033[0;33m'
__RESET = '\033[0m'

def _warn(message):
    sys.stdout.write(f"{__YELLOW}WARNING: {message}{__RESET}\n")

def _error(message):
    sys.stdout.write(f"{__RED}ERROR: {message}{__RESET}\n")

def _print(message):
    sys.stdout.write(f"{message}\n")