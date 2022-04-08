"""
> vdifheader - vdifheader.py
Defines VDIFHeader class that represents a single header within a VDIF file

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
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

from math import pow
from sys import stderr, stdout
from datetime import datetime, timedelta, timezone

from vdifheader.__utils__ import *
from vdifheader.vdifheaderfield import VDIFHeaderField

CHANNEL_LIMIT = 65536
FRAME_LIMIT = 134217728
HIGHEST_VERSION = 1
THREAD_LIMIT = 1024


class VDIFHeader:
    """A class that represents a single header within a VDIF file"""

    ######## PUBLIC FUNCTIONS

    def __init__(self):
        # header values
        self.invalid_flag = None
        self.legacy_mode = None
        self.seconds_from_epoch = None
        self.unassigned_field = None
        self.reference_epoch = None
        self.data_frame_number = None
        self.vdif_version = None
        self.num_channels = None
        self.data_frame_length = None
        self.data_type = None
        self.bits_per_sample = None
        self.thread_id = None
        self.station_id = None
        self.extended_data_version = None
        self.extended_data = None
        # utility values
        self.header_num = None
        self.warnings = []
        self.warnings_count = 0
        self.errors = []
        self.errors_count = 0
        self.raw_data = None

    @staticmethod
    def parse(raw_data, header_num=None):
        """Creates VDIFHeader object populated from values in raw data"""
        header = VDIFHeader()
        header.raw_data = switch_endianness(raw_data)
        header.header_num = header_num
        header.__parse_values()
        header.__validate_values()
        return header

    def get_timestamp(self):
        """Gets reference epoch + seconds from epoch as datetime object"""
        epoch = self.reference_epoch.value
        elapsed = timedelta(seconds=self.seconds_from_epoch.value)
        return epoch + elapsed

    def print_summary(self):
        """Prints warnings and errors found during validation"""
        for warning in self.warnings:
            message = f"WARNING: {warning} (header {self.header_num}).\n"
            stderr.write(colorify(message, Validity.UNKNOWN))
        for error in self.errors:
            message = f"ERROR: {error} (header {self.header_num}).\n"
            stderr.write(colorify(message, Validity.INVALID))

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
        self.__print_edv_values()

    def print_raw(self):
        """Prints raw binary header values, with coloring for validity"""
        word_num, word_bits = (0, 0)
        columns = "".join([f"     Byte {n}    |" for n in [3, 2, 1, 0]])
        output_string = f"       |{columns}\n"
        for field_name in self.__public_fields()[:-2]:
            if word_bits == 0:
                output_string += f"Word {word_num} "
            # get field values and color them as per validity
            field = getattr(self, field_name)
            raw = " ".join(reversed_bits(field.raw_value))
            output_string += f"|{colorify(raw, field.validity)}"
            word_bits += len(field.raw_value)
            # if at the end of a word, begin a new line
            if word_bits == WORD_BITS:
                word_num += 1
                output_string += f"|\n"
                word_bits = 0
        if self.legacy_mode.value != True:
            # print extended data version
            field = self.extended_data_version
            edv_raw = " ".join(reversed_bits(field.raw_value))
            output_string += f"Word 4 |{colorify(edv_raw, field.validity)}"
            # and then the data itself
            extended_data = reversed_bits(self.extended_data.raw_value)
            validity = self.extended_data.validity
            ed1 = colorify(" ".join(extended_data[0:24]), validity)
            ed2 = colorify(" ".join(extended_data[24:56]), validity)
            ed3 = colorify(" ".join(extended_data[56:88]), validity)
            ed4 = colorify(" ".join(extended_data[88:]), validity)
            output_string += f"|{ed1}|\nWord 5 |{ed2}|\n"
            output_string += f"Word 6 |{ed3}|\nWord 7 |{ed4}|\n"
        stdout.write(output_string)

    def print_verbose(self):
        """Prints a combination of raw, values, and summary output"""
        self.print_raw()
        self.print_values()
        self.print_summary()
        return

    ######## PRIVATE FUNCTIONS

    def __repr__(self):
        """Defines pretty print string representation of object"""
        repr_string = "<VDIFHeader"
        for field in self.public_fields():
            repr_string += "\n  "
            repr_string += repr(getattr(self, field))
        repr_string += ">"
        return repr_string

    def __str__(self):
        """Defines string representation of object"""
        return f"<VDIFHeader station_id={self.station_id},\
            timestamp={self.get_timestamp()}>"

    def __public_fields(self):
        """Gets field names, omitting utility fields such as errors count"""
        return ["invalid_flag", "legacy_mode", "seconds_from_epoch",
            "unassigned_field", "reference_epoch", "data_frame_number",
            "vdif_version", "num_channels", "data_frame_length", "data_type",
            "bits_per_sample", "thread_id", "station_id",
            "extended_data_version", "extended_data"]

    def __parse_values(self):
        """Gets and parses appropriate bits from raw data into header fields"""
        unknown = Validity.UNKNOWN
        # some values are booleans
        boolean_fields = ["invalid_flag", "legacy_mode"]
        for key in boolean_fields:
            int_value, raw = header_bits(self.raw_data, *header_position(key))
            field_object = VDIFHeaderField(key, (int_value == 1), raw, unknown)
            setattr(self, key, field_object)
        # some values are integers
        integer_fields = ["seconds_from_epoch", "unassigned_field",
            "data_frame_number", "vdif_version", "num_channels",
            "data_frame_length", "bits_per_sample", "thread_id",
            "extended_data_version"]
        for key in integer_fields:
            int_value, raw = header_bits(self.raw_data, *header_position(key))
            field_object = VDIFHeaderField(key, int_value, raw, unknown)
            setattr(self, key, field_object)
        # some values need scaling (as per the VDIF spec)
        self.num_channels.value = int(pow(2, self.num_channels.value))
        self.data_frame_length.value = self.data_frame_length.value * 8
        self.bits_per_sample.value = self.bits_per_sample.value + 1
        # some values need custom transformation
        key = "reference_epoch"
        int_value, raw = header_bits(self.raw_data, *header_position(key))
        year = 2000 + (int_value // 2)
        month = 1 if (int_value % 2 == 0) else 7
        date_value = datetime(year, month, day=1, tzinfo=timezone.utc)
        setattr(self, key, VDIFHeaderField(key, date_value, raw, unknown))
        key = "data_type"
        int_value, raw = header_bits(self.raw_data, *header_position(key))
        string_value = "complex" if (int_value == 1) else "real"
        setattr(self, key, VDIFHeaderField(key, string_value, raw, unknown))
        key = "station_id"
        _, raw = header_bits(self.raw_data, *header_position(key))
        string_value = convert_station_id(raw)
        setattr(self, key, VDIFHeaderField(key, string_value, raw, unknown))
        key = "extended_data"
        raw = header_extended_bits(self.raw_data)
        setattr(self, key, VDIFHeaderField(key, "(mixed data)", raw, unknown))
        return

    def __validate_values(self):
        """Assigns validity tests for each field based on VDIF spec"""
        # get current time, to check against if reference epoch in the future
        # yes, this is only set once. but that makes sense because if it was in
        # the future at any time after the file itself was formed, it's wrong
        epoch_limit = datetime.now(timezone.utc)
        frame_idx = self.header_num
        # now to set on each field: a test to run, ...
        # ... the validity to set if the test fails, ...
        # ... the message to add to warning or error log if it fails
        self.invalid_flag._set_validity_test(lambda x: not x, 
            Validity.UNKNOWN, "frame flagged as invalid by source")
        self.legacy_mode._set_validity_test(lambda x: not x, 
            Validity.UNKNOWN, "legacy format enabled")
        # TODO smarter multi-field checking for if epoch + elapsed is in future
        self.seconds_from_epoch._set_always_valid()
        self.unassigned_field._set_validity_test(lambda x: x == 0,
            Validity.INVALID, "synch code field contains incorrect value")
        self.reference_epoch._set_validity_test(lambda x: x <= epoch_limit,
            Validity.INVALID, "reference epoch is in the future")
        self.data_frame_number._set_validity_test(lambda x: x == frame_idx,
            Validity.UNKNOWN, "data frame number does not match index in file")
        self.vdif_version._set_validity_test(lambda x: x <= HIGHEST_VERSION, 
            Validity.INVALID, "specified vdif version does not exist")
        self.num_channels._set_validity_test(lambda x: x <= CHANNEL_LIMIT, 
            Validity.UNKNOWN, "num_channels exceeds soft cap")
        self.data_frame_length._set_validity_test(lambda x: x <= FRAME_LIMIT,
            Validity.INVALID, "data frame length exceeds limit")
        self.data_type._set_always_valid()
        self.bits_per_sample._set_always_valid()
        self.thread_id._set_validity_test(lambda x: x <= THREAD_LIMIT, 
            Validity.INVALID, "thread id exceeds limit")
        self.station_id._set_validity_test(lambda x: known_station_id(x),
            Validity.UNKNOWN,  "station id not in known list")
        self.extended_data_version._set_validity_test(lambda x: known_edv(x),
            Validity.INVALID, "specified extended data version does not exist")
        # TODO fine-grained validity checking as per EDV
        self.extended_data._set_always_valid()
        # now that they're set, here is where the checks actually run
        for field_name in self.__public_fields():
            self.__validate_field(field_name)
        return

    def __validate_field(self, field_name):
        """Runs stored validity test on field and stores message upon failure"""
        field = getattr(self, field_name)
        result, new_message = field._revalidate()
        if result == Validity.UNKNOWN:
            self.warnings.append(new_message)
            self.warnings_count += 1
        elif result == Validity.INVALID:
            self.errors.append(new_message)
            self.errors_count += 1
        return

    def __print_edv_values(self):
        """Prints any known extended data values, for print values output"""
        # TODO do that
        return
