from vdifheader.__utils__ import Validity, __validity_color, _DebugColor

__WORD_BYTES = 4

class VDIFHeaderField:
    '''A class that represents a single field within a VDIFHeader object'''

    ######## PUBLIC FUNCTIONS

    def __init__(self, name, value, raw_value, validity):
        self._name = name
        self.value = value
        self._raw_value = raw_value
        self._validity = validity

    ######## PRIVATE FUNCTIONS

    def __create_for(key, value, raw_value):
        header_field = VDIFHeaderField(key, value, raw_value, Validity.UNKNOWN)
        return header_field

    def __set_valid(self, valid=True):
        self._validity = Validity.VALID if valid else Validity.INVALID

    def __set_valid_nonstrict(self, valid=True):
        self._validity = Validity.VALID if valid else Validity.UNKNOWN

    def __is_valid(self):
        return self._validity == Validity.VALID

    def __raw_bits(self):
        if len(self.raw_value < __WORD_BYTES):
            # this must be a normal field
            color = __validity_color(self._validity)
            bytes = ' '.join(self._raw_value)
            return f"{color}{bytes}{_DebugColor.NONE}"
        else:
            # this must be extended data
            color = __validity_color(self._validity)
            start, end = (0, 24)
            output_string = ""
            for _ in range(4):
                byte = ' '.join(self._raw_value[start:end])
                output_string += f"|{color}{byte}{_DebugColor.NONE}|\n"
                end = start
                start += __WORD_BYTES
            return output_string

    def __repr__(self):
        return f"<VDIFHeaderField _name={self._name}, value={self.value}>"

    def __str__(self):
        return f"{self.value}"

    def __eq__(self, other):
        if other is VDIFHeaderField:
            return (
                self._name == other._name
                and self.value == other.value
                and self._raw_value == other._raw_value
                and self._validity == other._validity
            )
        else:
            return self.value == other