from math import pow

from vdifheader.__utils__ import __warn, __error, __print, __to_bin, Validity
from vdifheader.__parser__ import __parse, __validate

__WORD_BITS = 32


class VDIFHeader:
    """A class that represents a single header within a VDIF file"""

    ######## PUBLIC FUNCTIONS

    def __init__(self):
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
        self._extended_data = None
        self._header_num = 0
        self._warnings = []
        self._warnings_count = 0
        self._errors = []
        self._errors_count = []
        self._raw_data = None

    @staticmethod
    def parse(raw_data, header_num):
        header = VDIFHeader()
        header._raw_data = "".join([f"{b:08b}" for b in raw_data])
        header._header_num = header_num
        __parse(header)
        __validate(header)

    def get_timestamp(self):
        """Returns reference_epoch + seconds_from_epoch as datetime object"""
        # TODO get timestamp
        return

    def print_summary(self):
        """Prints warnings and errors found during validation"""
        for warning in self._warnings:
            __warn(warning)
        for error in self._errors:
            __error(error)
        __print(
            f"{self._errors_count} errors, "
            f"{self._warnings_count} warnings generated."
        )

    def print_values(self):
        """Prints key and value for each of the available header fields"""
        __print(f"Invalid flag: {self.invalid_flag}")
        __print(f"Legacy mode: {self.legacy_mode}")
        __print(f"Time from epoch: {self.seconds_from_epoch} seconds")
        # __print(f"Reference epoch: {}") # TODO
        __print(f"Data frame number: {self.data_frame_number}")
        __print(f"VDIF version: {self.vdif_version}")
        __print(f"Number of channels: {self.num_channels}")
        __print(f"Data frame length: {self.data_frame_length} bytes")
        __print(f"Data type: {'complex' if (self.data_type == 1) else 'real'}")
        __print(f"Bits per sample: {self.bits_per_sample}")
        __print(f"Thread ID: {self.thread_id}")
        __print(f"Station ID: {self.station_id}")
        __print(f"Extended data version: {self.extended_data_version}")
        self.__print_edv_values()

    def print_raw(self):
        """Prints raw binary header values, with coloring for validity"""
        raw_words = []
        if not self.legacy_mode and self._extended_data is not None:
            # TODO edv
            return

    def print_verbose(self):
        self.print_raw()
        self.print_values()
        self.print_summary()
        return

    ######## PRIVATE FUNCTIONS

    def __repr__(self):
        repr_string = "<VDIFHeader"
        for field in self.__public_fields():
            repr_string += "\n  "
            repr_string += repr(getattr(self, field))
        repr_string += ">"
        return repr_string

    def __str__(self):
        return f"<VDIFHeader station_id={self.station_id},\
            timestamp={self.get_timestamp()}>"

    def __print_edv_values():
        # TODO
        return

    def __public_fields(self):
        return [f for f in self.__dict__ if not f.startswith("_")]

    def __raw_frame(raw_words):
        __print(
            "         |     Byte 3    |     Byte 2    |"
            "     Byte 1    |     Byte 0    |"
        )
        for i in len(raw_words):
            __print(f"  Word {i} {raw_words[i]}")

    def __raw_word(fields):
        output_string = "|"
        for field in fields:
            output_string += field._raw_bits()
            output_string += "|"
        return output_string

    def __assert_(self, field_name, validator, message=None):
        _message = message
        field = self.getattr(field_name)
        field.__set_valid(validator(field.value))
        if not field.__is_valid():
            if message is None:
                _message = f"invalid value for {field_name}."
            self._errors.append(_message)
            self._errors_count += 1

    def __assert_nonstrict(self, field_name, validator, message=None):
        _message = message
        field = self.getattr(field_name)
        field.__set_valid_nonstrict(validator(field.value))
        if not field.__is_valid():
            if message is None:
                _message = f"unverifiable value for {field_name}."
            self._warnings.append(_message)
            self._warnings_count += 1

    def __get_bits(self, word, start, end=None):
        _end = start + 1 if end == None else end + 1
        word = self._raw_data[(word + 1) * __WORD_BITS : word * __WORD_BITS : -1]
        bits = "".join(word[start:end])  # the bits to be printed (big endian)
        bits_reversed = "".join(word[end:start:-1])  # bits to interpret (little)
        return (int(bits_reversed, 2), bits)

    def __get_ed_bits(self):
        _, raw_value = self.__get_bits(4, 0, 23)
        for word in range(4, 7):
            _, _raw_value = self.__get_bits(word, 0, 31)
            raw_value += _raw_value
        return None, raw_value
