# > vdifheader - __utils__.py
# Defines utility functions for tasks such as bit and color manipulation

# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

"""
> vdifheader - __utils__.py (private)
Defines utility functions for tasks such as bit and color manipulation
"""
__author__ = "Mars Buttfield-Addison"
__authors__ = [__author__]
__contact__ = "hello@themartianlife.com"
__copyright__ = f"Copyright 2022, {__author__}"
__credits__ = __authors__
__date__ = "2022/04/07"
__deprecated__ = False
__email__ = __contact__
__license__ = "GPLv3"
__maintainer__ = __author__
__status__ = "Pre-release"
__version__ = "0.1"

from enum import Enum

try:  # colors if they have them
    import colorama
    colorama.init()
except:  # else don't worry about it
    pass

WORD_BITS = 32
WORD_BYTES = 4
HEADER_WORDS = 8


class Validity(Enum):
    UNKNOWN = 0
    INVALID = 1
    VALID = 2


class __DebugColor:
    YELLOW = "\033[0;33m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    NONE = "\033[0m"


def colorify(message, color):
    """Prepends corresponding ANSI color code, appends style reset code"""
    if color == __DebugColor.YELLOW or color == Validity.UNKNOWN:
        return f"{__DebugColor.YELLOW}{message}{__DebugColor.NONE}"
    elif color == __DebugColor.RED or color == Validity.INVALID:
        return f"{__DebugColor.RED}{message}{__DebugColor.NONE}"
    elif color == __DebugColor.GREEN or color == Validity.VALID:
        return f"{__DebugColor.GREEN}{message}{__DebugColor.NONE}"
    else:
        return message


def switch_endianness(raw_data):
    """Reverses the bits in each word but retains word order"""
    data = list(raw_data)
    switched_data = []
    for word in range(HEADER_WORDS):
        word_data = data[word * WORD_BYTES: (word + 1) * WORD_BYTES]
        switched_word = reversed(word_data)
        binary_word = "".join([f"{x:08b}" for x in switched_word])
        switched_data.append(binary_word)
    return switched_data


def header_bits(raw_data, word, start_bit, num_bits):
    """Accesses bits within two-dimensional raw data"""
    word_data = reversed_bits(raw_data[word])
    bits = reversed_bits(word_data[start_bit: start_bit + num_bits])
    return (int(bits, 2), bits)


def header_extended_bits(raw_data):
    """Accesses bits 128-255 of raw data, omitting bits 152-159"""
    bits = ""
    for word in range(4, 8):
        word_r = raw_data[word]
        if word == 4: # if this is the first word of extended_data
            word_r = word_r[0:24]  # remove the extended_data_version field
        bits += word_r # otherwise add the whole thing
    return bits


def header_position(key):
    """Returns word number, starting bit number, and count of bits for key"""
    positions = {  # word, start_bit, num_bits
        "invalid_flag": (0, 31, 1),
        "legacy_mode": (0, 30, 1),
        "seconds_from_epoch": (0, 0, 30),
        "unassigned_field": (1, 30, 2),
        "reference_epoch": (1, 24, 6),
        "data_frame_number": (1, 0, 24),
        "vdif_version": (2, 29, 3),
        "num_channels": (2, 24, 5),
        "data_frame_length": (2, 0, 24),
        "data_type": (3, 31, 1),
        "bits_per_sample": (3, 26, 5),
        "thread_id": (3, 16, 10),
        "station_id": (3, 0, 16),
        "extended_data_version": (4, 24, 8),
    }
    return positions[key]


def convert_station_id(raw_id):
    """Converts raw id to unsigned int or 2-char ASCII, depending on value"""
    char1 = int(raw_id[0:8], 2)
    char2 = int(raw_id[8:16], 2)
    if char2 != 48:  # where char2 == ASCII 0x30 means "treat this as int"
        return f"{chr(char1)}{chr(char2)}"
    else:
        return f"{int(raw_id, 2)}"


def known_station_id(station_id):
    """Checks for station id in included list of known ids"""
    # TODO better central source of more station codes? these ones are from IVS
    # TODO also consider possible mark4 transformation mangling?
    # e.g. www.atnf.csiro.au/vlbi/dokuwiki/doku.php/difx/difx2mark4/stationcodes
    known_ids = ["Oh", "Sy", "Ag", "Hb", "Ho", "Ke", "Yg", "Pa", "Ft", "Ur", 
        "Sh", "Mh", "Eb", "Wz", "Mc", "Nt", "Ma", "Kb", "K1", "Kg", "Ts", "Is", 
        "Mn", "Ww", "Ny", "Bd", "Sv", "Zc", "Yb", "Hh", "Kv", "On", "Sm", "Gs", 
        "Gg", "Wf", "Kk", "Mp"]
    return (station_id in known_ids)


def known_edv(extended_data_version):
    """Checks for extended data version in included list of known version ids"""
    known_edvs = [0x00, 0x01, 0x02, 0x03, 0x04, 0xab]
    return (extended_data_version in known_edvs)


def reversed_bits(binary_string):
    return "".join(reversed(binary_string))
