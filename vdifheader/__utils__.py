from sys import stdout
from enum import Enum

class Validity(Enum):
    INVALID = 0
    VALID = 1
    UNKNOWN = 3

class _DebugColor(Enum):
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[0;33m'
    NONE = '\033[0m'

def __warn(message):
    stdout.write(f"{_DebugColor.YELLOW}WARNING: {message}{_DebugColor.NONE}\n")

def __error(message):
    stdout.write(f"{_DebugColor.RED}ERROR: {message}{_DebugColor.NONE}\n")

def __print(message):
    stdout.write(f"{message}\n")

def __validity_color(validity):
    if validity == Validity.VALID:
        return _DebugColor.GREEN
    elif validity == Validity.INVALID:
        return _DebugColor.RED
    elif validity == Validity.UNKNOWN:
        return _DebugColor.YELLOW
    else:
        return _DebugColor.NONE 

def __to_bin(raw_data):
        return ''.join([f"{b:08b}" for b in raw_data])