# > vdifheader - vdifheader.py
# Defines VDIFHeader class that represents a single header within a VDIF file

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
> vdifheader - vdifheader.py
Defines VDIFHeader class that represents a single header within a VDIF file
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

from math import log2
from sys import stdout
from datetime import datetime, timedelta
from typing import Any, Union

from vdifheader._utils import *
from vdifheader.vdifheaderfield import VDIFHeaderField as Field


HIGHEST_VERSION = 1     # highest vdif version that is recognised
WORD_BYTES = 4          # number of bytes in a word
WORD_BITS = 32          # number of bits in a word
HEADER_WORDS = 8        # number of words in a (non-legacy) header


class VDIFHeader:
    """A class that represents a single header within a VDIF file"""

    def __init__(self, valid_caller: bool=False):
        """Private initialiser that raises NotImplementedError on direct call"""
        if not valid_caller:
            raise NotImplementedError("VDIFHeader object cannot be directly " \
                "instatiated. Values must be extracted using factory method " \
                "VDIFHeader.parse().")
        # raw binary data
        self.__raw_values: dict[str,str] = {}
        # actual field values
        self.__bool_fields: dict[Field,bool] = {}
        self.__datetime_fields: dict[Field,datetime] = {}
        self.__int_fields: dict[Field,int] = {}
        self.__str_fields: dict[Field,str] = {}
        self.__extended_data_fields: dict[Field,type] = {}
        return

    @staticmethod
    def parse(raw_data: bytes) -> "VDIFHeader":
        """Creates new VDIFHeader object from interpretation of raw data"""
        header = VDIFHeader(valid_caller=True)
        binary_data = VDIFHeader._preprocess(raw_data)
        # set each of the boolean fields
        bool_fields = [Field.INVALID_FLAG, Field.LEGACY_MODE]
        for field in bool_fields:
            header._try_set_field(field, field._from(binary_data))
        # now datetime fields
        datetime_fields = [Field.REFERENCE_EPOCH]
        for field in datetime_fields:
            header._try_set_field(field, field._from(binary_data))
        # now integer fields
        int_fields = [Field.SECONDS_FROM_EPOCH, Field.UNASSIGNED_FIELD, 
            Field.DATA_FRAME_NUMBER, Field.VDIF_VERSION, Field.NUM_CHANNELS, 
            Field.DATA_FRAME_LENGTH, Field.BITS_PER_SAMPLE, Field.THREAD_ID,
            Field.EXTENDED_DATA_VERSION]
        for field in int_fields:
            header._try_set_field(field, field._from(binary_data))
        # now string fields
        str_fields = [Field.DATA_TYPE, Field.STATION_ID]
        for field in str_fields:
            header._try_set_field(field, field._from(binary_data))
        header.__extended_data_fields = Field.EXTENDED_DATA._from(binary_data)
        raw_extended_data = Field.EXTENDED_DATA._raw_from(binary_data)
        header.__raw_values[Field.EXTENDED_DATA] = raw_extended_data
        return header

    ######## PROPERTIES

    @property
    def invalid_flag(self) -> bool:
        """Whether data source device believes this frame is corrupted"""
        return self.__bool_fields[Field.INVALID_FLAG]

    @invalid_flag.setter
    def invalid_flag(self, value: bool):
        self._try_set_field(Field.INVALID_FLAG, value)
        return

    @property
    def legacy_mode(self) -> bool:
        """Whether this header uses the legacy 16-byte format"""
        return self.__bool_fields[Field.LEGACY_MODE]

    @legacy_mode.setter
    def legacy_mode(self, value: bool):
        self._try_set_field(Field.LEGACY_MODE, value)
        return

    @property
    def seconds_from_epoch(self) -> int:
        """Seconds offset from this headers's reference epoch"""
        return self.__int_fields[Field.SECONDS_FROM_EPOCH]

    @seconds_from_epoch.setter
    def seconds_from_epoch(self, value: int):
        self._try_set_field(Field.SECONDS_FROM_EPOCH, value)
        return

    @property
    def unassigned_field(self) -> int:
        """Synch code field that should be all zeroes"""
        return self.__int_fields[Field.UNASSIGNED_FIELD]

    @unassigned_field.setter
    def unassigned_field(self, value: int):
        if type(value) == int and value != 0:
            vh_error("unassigned_field value should always be 0")
        self._try_set_field(Field.UNASSIGNED_FIELD, value)
        return

    @property
    def reference_epoch(self) -> datetime:
        """Datetime indicating point from which seconds from epoch begins"""
        return self.__datetime_fields[Field.REFERENCE_EPOCH]

    @reference_epoch.setter
    def reference_epoch(self, value: datetime):
        now = to_utc(datetime.now())
        _value = value
        if type(value) == datetime:
            _value = to_utc(value)
            if _value > now:
                vh_warn("reference_epoch should not be in the future")
            if _value.year < 2000:
                raise ValueError("reference_epoch can only be post-2000.")
            if _value.month not in [1, 7] or _value.day != 1:
                raise ValueError("reference_epoch can only be Jan or Jul 1st.")
        self._try_set_field(Field.REFERENCE_EPOCH, _value)
        return

    @property
    def data_frame_number(self) -> int:
        """Index of this data frame in overall data stream"""
        return self.__int_fields[Field.DATA_FRAME_NUMBER]

    @data_frame_number.setter
    def data_frame_number(self, value: int):
        self._try_set_field(Field.DATA_FRAME_NUMBER, value)
        return

    @property
    def vdif_version(self) -> int:
        """Version of VDIF format specification to apply in interpretation"""
        return self.__int_fields[Field.VDIF_VERSION]

    @vdif_version.setter
    def vdif_version(self, value: int):
        if type(value) == int and value > HIGHEST_VERSION:
            vh_warn(f"vdif_version value > {HIGHEST_VERSION} not recognised")
        self._try_set_field(Field.VDIF_VERSION, value)
        return

    @property
    def num_channels(self) -> int:
        """Number of channels in data stream"""
        return self.__int_fields[Field.NUM_CHANNELS]

    @num_channels.setter
    def num_channels(self, value: int):
        if type(value) == int and not log2(value).is_integer():
            raise ValueError(f"num_channels must be power of 2.")
        self._try_set_field(Field.NUM_CHANNELS, value)
        return

    @property
    def data_frame_length(self) -> int:
        """Length of this frame in bytes, including header"""
        return self.__int_fields[Field.DATA_FRAME_LENGTH]

    @data_frame_length.setter
    def data_frame_length(self, value: int):
        if type(value) == int:
            min_length = 16 if self.legacy_mode else 32
            if value < min_length:
                raise ValueError(f"data_frame_length must be > {min_length}.")
            elif value % 8 != 0:
                raise ValueError("data_frame_length must be multiple of 8.")
        self._try_set_field(Field.DATA_FRAME_LENGTH, value)
        return

    @property
    def data_type(self) -> str:
        """Indicates whether stream represents real or complex numbers"""
        return self.__str_fields[Field.DATA_TYPE]

    @data_type.setter
    def data_type(self, value: str):
        if type(value) == str and value != "real" and value != "complex":
            raise ValueError(f"Cannot assign value {value} to field " \
                f"data_type with expected values=['real'|'complex'].") 
        self._try_set_field(Field.DATA_TYPE, value)
        return

    @property
    def bits_per_sample(self) -> int:
        """Number of bits used to represent a single sample in data stream"""
        return self.__int_fields[Field.BITS_PER_SAMPLE]

    @bits_per_sample.setter
    def bits_per_sample(self, value: int):
        if type(value) == int and value < 1:
            raise ValueError("bits_per_sample must be >= 1.")
        self._try_set_field(Field.BITS_PER_SAMPLE, value)
        return

    @property
    def thread_id(self) -> int:
        """Index of this frame's data thread in overall data stream"""
        return self.__int_fields[Field.THREAD_ID]

    @thread_id.setter
    def thread_id(self, value: int):
        self._try_set_field(Field.THREAD_ID, value)
        return

    @property
    def station_id(self) -> str:
        """2-char ASCII or unsigned int code representing data source device"""
        return self.__str_fields[Field.STATION_ID]

    @station_id.setter
    def station_id(self, value: str):
        if type(value) == str:
            if value.isnumeric() and int(value) // 256 >= 0x30:
                raise ValueError("numeric station_id first bit must be < 0x30.")
            elif not value.isnumeric() and len(value) != 2:
                raise ValueError("ASCII station_id length must be 2 chars.")
        self._try_set_field(Field.STATION_ID, value)
        return

    @property
    def extended_data_version(self) -> int:
        """Extended data format to apply in extended data interpretation"""
        return self.__int_fields[Field.EXTENDED_DATA_VERSION]

    @extended_data_version.setter
    def extended_data_version(self, new_value: int):
        recognised_versions = [0x00, 0x01, 0x02, 0x03, 0x04, 0xab]
        if new_value not in recognised_versions:
            vh_warn(f"extended_data_version {new_value} not recognised")
        self._try_set_field(Field.EXTENDED_DATA_VERSION, new_value)
        self.__interpret_extended_data()
        return

    @property
    def extended_data(self) -> int:
        """Extended data dict, interpreted as per extended data version"""
        return self.__extended_data_fields

    @extended_data.setter
    def extended_data(self, new_value: dict[Field,Any]):
        raise NotImplementedError("Cannot directly set extended_data value.")
        # TODO implement this

    @property
    def to_dict(self) -> dict[Field,Any]:
        """Creates dict of header fields as format field: field_value"""
        fields = self.__bool_fields | self.__datetime_fields
        fields = fields | self.__int_fields | self.__str_fields
        fields[Field.EXTENDED_DATA] = self.__extended_data_fields
        return fields

    ######## PUBLIC METHODS

    def get_timestamp(self) -> datetime:
        """Gets reference epoch + seconds from epoch as datetime object"""
        epoch = self.reference_epoch
        elapsed = timedelta(seconds=self.seconds_from_epoch)
        return epoch + elapsed

    def get_station_information(self) -> str:
        """Gets name of source station for given station id, if known"""
        return station_information(self.station_id)

    def to_inifile(self, output_filepath: str):
        """Writes file of name=value for each field in header"""
        with open(sanitized_path(output_filepath), "w+") as output_file:
            for field_name, field_value in self.to_dict.items():
                if type(field_value) is bool:
                    field_value = str(field_value).lower()
                elif type(field_value) is datetime:
                    field_value = str(field_value.date())
                output_file.write(f"{field_name}={field_value}\n")
        return

    def to_csv(self, output_filepath: str):
        """Writes file of field_name,field_value for each field in header"""
        with open(sanitized_path(output_filepath), "w+") as output_file:
            output_file.write("field_name,field_value\n")
            for field_name, field_value in self.to_dict.items():
                output_file.write(f"{field_name},{field_value}\n")
        return

    def print_values(self):
        """Prints key and value for each of the available header fields"""
        stdout.write(f"Invalid flag: {self.invalid_flag}\n")
        stdout.write(f"Legacy mode: {self.legacy_mode}\n")
        stdout.write(f"Time from epoch: {self.seconds_from_epoch} seconds\n")
        stdout.write(f"Reference epoch: {self.reference_epoch} UTC\n")
        stdout.write(f"Data frame number: {self.data_frame_number}\n")
        stdout.write(f"VDIF version: {self.vdif_version}\n")
        stdout.write(f"Number of channels: {self.num_channels}\n")
        stdout.write(f"Data frame length: {self.data_frame_length} bytes\n")
        stdout.write(f"Data type: {self.data_type}\n")
        stdout.write(f"Bits per sample: {self.bits_per_sample} bit(s)\n")
        stdout.write(f"Thread ID: {self.thread_id}\n")
        stdout.write(f"Station ID: {self.station_id}\n")
        stdout.write(f"Extended data version: {self.extended_data_version}\n")
        self.__print_extended_data_values()
        return

    def print_binary(self):
        column_nums = "".join([f"     Byte {n}    |" for n in [3, 2, 1, 0]])
        stdout.write(f"       |{column_nums}\n")
        for word in range(8):
            self.__print_binary_word(word)
        return

    ######## PRIVATE METHODS

    @staticmethod
    def _preprocess(raw_data: bytes) -> str:
        data = list(raw_data)
        switched_data = ""
        for word in range(HEADER_WORDS):
            word_data = data[word * WORD_BYTES: (word + 1) * WORD_BYTES]
            for byte in word_data:
                switched_data += switch_end(f"{byte:08b}")
        return switched_data

    def _try_set_field(self, field: Field, 
            new_value: Union[bool,datetime,int,str]):
        if field not in Field.primary_values(): # an assignable field
            raise ValueError("_try_set_field cannot assign value to field " \
                f"{field.value}.")
        if type(new_value) != field.data_type: # correct type of value
            raise TypeError("_try_set_field cannot assign value of type " \
                f"{type(new_value)} to field of type {field.data_type}.")         
        raw_value = switch_end(field._encoder(new_value))
        if len(raw_value) > field._bit_length: # fits within bit space
            raise ValueError(f"Cannot assign value {new_value} to field " \
                f"{field.value} with maximum bit length {field._bit_length}.")
        raw_value = raw_value.ljust(field._bit_length, "0")
        # otherwise, value is good
        if field.data_type == bool:      
            self.__bool_fields[field] = new_value
        elif field.data_type == datetime: 
            self.__datetime_fields[field] = new_value
        elif field.data_type == int: 
            if new_value < 0:
                raise ValueError(f"Cannot negative value {new_value} to " \
                    f"field {field.value}.")
            self.__int_fields[field] = new_value
        elif field.data_type == str: 
            self.__str_fields[field] = new_value
        # only get here if haven't errored in assignment of incorrect type
        self.__raw_values[field] = raw_value
        return

    def _get_value(self, field: Field):
        if field.data_type == bool:      
            return self.__bool_fields.get(field, None)
        elif field.data_type == datetime: 
            return self.__datetime_fields.get(field, None)
        elif field.data_type == int: 
            return self.__int_fields.get(field, None)
        elif field.data_type == str: 
            return self.__str_fields.get(field, None)
        elif field == Field.EXTENDED_DATA:
            return self.__extended_data_fields

    def _get_raw_value(self, field: Field):
        return self.__raw_values.get(field, None)

    def __interpret_extended_data(self):
        raw_value = switch_end(self.__raw_values[Field.EXTENDED_DATA])
        edv = self.extended_data_version
        extended_data = Field.EXTENDED_DATA._decoder((raw_value, edv))
        self.__extended_data_fields = extended_data
        return

    def __print_binary_word(self, word_num: int):
        word_content = ""
        word_fields = []
        if word_num == 0:
            word_fields = [Field.INVALID_FLAG, Field.LEGACY_MODE, 
                Field.SECONDS_FROM_EPOCH]
        elif word_num == 1:
            word_fields = [Field.UNASSIGNED_FIELD, Field.REFERENCE_EPOCH, 
                Field.DATA_FRAME_NUMBER]
        elif word_num == 2:
            word_fields = [Field.VDIF_VERSION, Field.NUM_CHANNELS, 
                Field.DATA_FRAME_LENGTH]
        elif word_num == 3:
            word_fields = [Field.DATA_TYPE, Field.BITS_PER_SAMPLE, 
                Field.THREAD_ID, Field.STATION_ID]
        word_sequences = [self._get_raw_value(field) for field in word_fields]
        if word_num == 4:
            word_sequences = [self._get_raw_value(Field.EXTENDED_DATA_VERSION)]
            word_sequences += [self._get_raw_value(Field.EXTENDED_DATA)[:24]]
        elif word_num >= 5:
            start = 24 + ((word_num - 5) * WORD_BITS)
            end = start + WORD_BITS
            word = self._get_raw_value(Field.EXTENDED_DATA)[start:end]
            word_sequences = [word]
        for sequence in word_sequences:
            word_content += f"|{' '.join(sequence)}"
        stdout.write(f"Word {word_num} {word_content}|\n")
        return

    ######## OVERLOADED METHODS

    def __eq__(self, other: "VDIFHeader") -> bool:
        return (isinstance(other, VDIFHeader) and
            self.__bool_fields == other.__bool_fields and
            self.__datetime_fields == other.__datetime_fields and
            self.__int_fields == other.__int_fields and
            self.__str_fields == other.__str_fields and
            self.__extended_data_fields == other.__extended_data_fields)

    ######## NOT IMPLEMENTED METHODS

    def __print_extended_data_values(self):
        sample_rate = self.extended_data.get(Field.SAMPLE_RATE, None)
        sample_rate_unit = self.extended_data.get(Field.SAMPLE_RATE_UNIT, None)
        if sample_rate is not None and sample_rate_unit is not None:
            stdout.write(f"Sample rate: {sample_rate} {sample_rate_unit}\n")
        # TODO implement others
        return
