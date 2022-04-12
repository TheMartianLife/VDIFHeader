# > vdifheader - vdifheaderfield.py
# Defines VDIFHeaderField class that represents a single field within a VDIFHeader

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
> vdifheader - vdifheaderfield.py
Defines VDIFHeaderField class that represents a single field within a VDIFHeader
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
from math import log2, pow
from datetime import datetime, timezone
from typing import Any, Callable, Tuple, Union

from vdifheader._utils import switch_end, to_utc

WORD_BITS = 32      # number of bits in a word
ED_START = 128      # start bit of extended data field
ED_PAUSE = 152      # start of extended data version field
ED_UNPAUSE = 160    # end of extended data version field


class VDIFHeaderField(Enum):
    INVALID_FLAG = "invalid_flag"
    LEGACY_MODE = "legacy_mode"
    SECONDS_FROM_EPOCH = "seconds_from_epoch"
    UNASSIGNED_FIELD = "unassigned_field"
    REFERENCE_EPOCH = "reference_epoch"
    DATA_FRAME_NUMBER = "data_frame_number"
    VDIF_VERSION = "vdif_version"
    NUM_CHANNELS = "num_channels"
    DATA_FRAME_LENGTH = "data_frame_length"
    DATA_TYPE = "data_type"
    BITS_PER_SAMPLE = "bits_per_sample"
    THREAD_ID = "thread_id"
    STATION_ID = "station_id"
    EXTENDED_DATA_VERSION = "extended_data_version"
    EXTENDED_DATA = "extended_data"
    SAMPLE_RATE = "sample_rate"
    SAMPLE_RATE_UNIT = "sample_rate_unit"

    ######## STATIC METHODS

    @classmethod
    def all_values(cls):
        return [field for field in cls]

    @classmethod
    def primary_values(cls):
        return VDIFHeaderField.all_values()[:14]

    @classmethod
    def optional_values(cls):
        return VDIFHeaderField.all_values()[15:]

    ######## PUBLIC PROPERTIES

    @property
    def data_type(self) -> type:
        bool_fields = [VDIFHeaderField.INVALID_FLAG, 
            VDIFHeaderField.LEGACY_MODE]
        if self in bool_fields: return bool
        datetime_fields = [VDIFHeaderField.REFERENCE_EPOCH]
        if self in datetime_fields: return datetime
        int_fields = [VDIFHeaderField.SECONDS_FROM_EPOCH, 
            VDIFHeaderField.UNASSIGNED_FIELD, VDIFHeaderField.DATA_FRAME_NUMBER,
            VDIFHeaderField.VDIF_VERSION, VDIFHeaderField.NUM_CHANNELS, 
            VDIFHeaderField.DATA_FRAME_LENGTH, VDIFHeaderField.BITS_PER_SAMPLE,
            VDIFHeaderField.THREAD_ID, VDIFHeaderField.EXTENDED_DATA_VERSION]
        if self in int_fields: return int
        str_fields = [VDIFHeaderField.DATA_TYPE, 
            VDIFHeaderField.STATION_ID]
        if self in str_fields: return str
        return

    ######## PRIVATE PROPERTIES

    @property
    def _bit_length(self) -> int:
        bit_lengths = {
            VDIFHeaderField.INVALID_FLAG: 1,
            VDIFHeaderField.LEGACY_MODE: 1,
            VDIFHeaderField.SECONDS_FROM_EPOCH: 30,
            VDIFHeaderField.UNASSIGNED_FIELD: 2,
            VDIFHeaderField.REFERENCE_EPOCH: 6,
            VDIFHeaderField.DATA_FRAME_NUMBER: 24,
            VDIFHeaderField.VDIF_VERSION: 3,
            VDIFHeaderField.NUM_CHANNELS: 5,
            VDIFHeaderField.DATA_FRAME_LENGTH: 24,
            VDIFHeaderField.DATA_TYPE: 1,
            VDIFHeaderField.BITS_PER_SAMPLE: 5,
            VDIFHeaderField.THREAD_ID: 10,
            VDIFHeaderField.STATION_ID: 16,
            VDIFHeaderField.EXTENDED_DATA_VERSION: 8,
            VDIFHeaderField.EXTENDED_DATA: 120,
        }
        return bit_lengths[self]

    @property
    def _encoder(self) -> Callable:
        bit_length = self._bit_length
        _simple_bools = [
            VDIFHeaderField.INVALID_FLAG, 
            VDIFHeaderField.LEGACY_MODE,            
        ]
        if self in _simple_bools: # convert to int and then 1-bit string 
            return (lambda x: f"{int(x)}")
        _simple_ints = [
            VDIFHeaderField.INVALID_FLAG, 
            VDIFHeaderField.LEGACY_MODE,
            VDIFHeaderField.SECONDS_FROM_EPOCH,
            VDIFHeaderField.UNASSIGNED_FIELD,
            VDIFHeaderField.DATA_FRAME_NUMBER,
            VDIFHeaderField.VDIF_VERSION,
            VDIFHeaderField.THREAD_ID,
            VDIFHeaderField.EXTENDED_DATA_VERSION,
        ]
        if self in _simple_ints: # convert to bit string
            return (lambda x: format(x, "b"))
        encoders = { # otherwise use specialised encoder
            VDIFHeaderField.REFERENCE_EPOCH: self._encoder_reference_epoch,
            VDIFHeaderField.NUM_CHANNELS: 
                (lambda x: format(int(log2(x)), "b")),
            VDIFHeaderField.DATA_FRAME_LENGTH: 
                (lambda x: format(x // 8, "b")),
            VDIFHeaderField.DATA_TYPE: (lambda x: "0" if x == "real" else "1"),
            VDIFHeaderField.BITS_PER_SAMPLE: 
                (lambda x: format(x - 1, "b")),
            VDIFHeaderField.STATION_ID:  self._encoder_station_id,
            VDIFHeaderField.EXTENDED_DATA: self._encoder_extended_data,
        }
        return encoders[self]

    @property
    def _decoder(self) -> Callable:
        _simple_bools = [
            VDIFHeaderField.INVALID_FLAG, 
            VDIFHeaderField.LEGACY_MODE,            
        ]
        if self in _simple_bools: # convert to int and then compare as bool
            return (lambda x: int(x) == 1)
        _simple_ints = [
            VDIFHeaderField.INVALID_FLAG, 
            VDIFHeaderField.LEGACY_MODE,
            VDIFHeaderField.SECONDS_FROM_EPOCH,
            VDIFHeaderField.UNASSIGNED_FIELD,
            VDIFHeaderField.DATA_FRAME_NUMBER,
            VDIFHeaderField.VDIF_VERSION,
            VDIFHeaderField.THREAD_ID,
            VDIFHeaderField.EXTENDED_DATA_VERSION,
        ]
        if self in _simple_ints: # convert straight to int at base 2
            return (lambda x: int(x, 2))
        decoders = { # otherwise use specialised encoder
            VDIFHeaderField.REFERENCE_EPOCH: self._decoder_reference_epoch,
            VDIFHeaderField.NUM_CHANNELS: (lambda x: int(pow(2, int(x, 2)))),
            VDIFHeaderField.DATA_FRAME_LENGTH: (lambda x: int(x, 2) * 8),
            VDIFHeaderField.DATA_TYPE: 
                (lambda x: "complex" if int(x) == 1 else "real"),
            VDIFHeaderField.BITS_PER_SAMPLE: (lambda x: int(x, 2) + 1),
            VDIFHeaderField.STATION_ID: self._decoder_station_id,
            VDIFHeaderField.EXTENDED_DATA: self._decoder_extended_data,
        }
        return decoders[self]

    @property
    def _header_position(self) -> Tuple[int,int]:
        header_positions = {
            VDIFHeaderField.INVALID_FLAG: (0, 31),
            VDIFHeaderField.LEGACY_MODE: (0, 30),
            VDIFHeaderField.SECONDS_FROM_EPOCH: (0, 0),
            VDIFHeaderField.UNASSIGNED_FIELD: (1, 30),
            VDIFHeaderField.REFERENCE_EPOCH: (1, 24),
            VDIFHeaderField.DATA_FRAME_NUMBER: (1, 0),
            VDIFHeaderField.VDIF_VERSION: (2, 29),
            VDIFHeaderField.NUM_CHANNELS: (2, 24),
            VDIFHeaderField.DATA_FRAME_LENGTH: (2, 0),
            VDIFHeaderField.DATA_TYPE: (3, 31),
            VDIFHeaderField.BITS_PER_SAMPLE: (3, 26),
            VDIFHeaderField.THREAD_ID: (3, 16),
            VDIFHeaderField.STATION_ID: (3, 0),
            VDIFHeaderField.EXTENDED_DATA_VERSION: (4, 24),
            VDIFHeaderField.EXTENDED_DATA: (4, 0),
        }
        return header_positions[self]

    @property
    def _encoder_reference_epoch(self) -> Callable:
        return (lambda x: VDIFHeaderField._encode_reference_epoch(x))

    @property
    def _decoder_reference_epoch(self) -> Callable:
        return (lambda x: VDIFHeaderField._decode_reference_epoch(x))

    @property
    def _encoder_station_id(self) -> Callable:
        return (lambda x:
            format(int(x), "b") if x.isnumeric() 
            else VDIFHeaderField._encode_ascii(x)
        )

    @property
    def _decoder_station_id(self) -> Callable:
        return (lambda x:
            f"{int(x)}" if int(x[-8:], 2) < 48
            else VDIFHeaderField._decode_ascii(x)
        )

    @property
    def _encoder_extended_data(self) -> Callable:
        return (lambda x: VDIFHeaderField._encode_extended_data(x))

    @property
    def _decoder_extended_data(self) -> Callable:
        return (lambda x: VDIFHeaderField._decode_extended_data(*x))

    ######## PRIVATE METHODS

    def _from(self, raw_data: str) -> Union[bool,datetime,int,str]:
        raw_value = self._raw_from(raw_data)
        if raw_value == "":
            raise ValueError(f"{self.value} cannot be empty")
        if self == VDIFHeaderField.EXTENDED_DATA:
            edv = VDIFHeaderField.EXTENDED_DATA_VERSION._from(raw_data)
            return self._decoder((switch_end(raw_value), edv))
        return self._decoder(switch_end(raw_value))

    def _raw_from(self, raw_data: str) -> str:
        if self == VDIFHeaderField.EXTENDED_DATA:
            word4 = "".join(raw_data[ED_START:ED_PAUSE])
            words5_7 = "".join(raw_data[ED_UNPAUSE:])
            return word4 + words5_7
        word, bit = self._header_position
        start = (word * WORD_BITS) + bit
        end = start + self._bit_length
        raw_value = raw_data[start:end]
        return raw_value

    ######## PRIVATE STATIC METHODS

    @staticmethod
    def _encode_reference_epoch(epoch: datetime) -> str:
        _epoch = to_utc(epoch)
        years = (_epoch.year - 2000) * 2
        month_offset = 1 if (_epoch.month == 7) else 0
        return format(years + month_offset, "b")

    @staticmethod
    def _decode_reference_epoch(raw_data: str) -> datetime:
        int_value = int(raw_data, 2)
        year = 2000 + (int_value // 2)
        month = 7 if (int_value % 2 == 1) else 1
        return datetime(year, month, day=1, tzinfo=timezone.utc)

    @staticmethod
    def _encode_extended_data(raw_data: str) -> str:
        # TODO support extended_data fields
        return

    @staticmethod
    def _decode_extended_data(raw_data: str, 
            version: int=0) -> dict["VDIFHeaderField",Any]:
        extended_data = {}
        if version == 0x01:
            pass # TODO support extended_data fields
        elif version == 0x02:
            pass # TODO support extended_data fields
        elif version == 0x03:
            pass # TODO support extended_data fields
        elif version == 0x04:
            pass # TODO support extended_data fields
        elif version == 0xab:
            pass # TODO support extended_data fields
        return extended_data

    @staticmethod
    def _encode_ascii(ascii_string: str) -> str:
        binary_string = ""
        for character in reversed(ascii_string):
            binary_string += format(ord(character), "08b")
        return binary_string

    @staticmethod
    def _decode_ascii(binary_string: str) -> str:
        ascii_string = ""
        if len(binary_string) % 8 != 0:
            raise ValueError("__decode_ascii requires binary_string length " \
                "to be a multiple of 8 bits.")
        for i in range(len(binary_string) // 8):
            int_value = int(binary_string[i * 8:(i + 1) * 8], 2)
            ascii_string += chr(int_value)
        return ascii_string
