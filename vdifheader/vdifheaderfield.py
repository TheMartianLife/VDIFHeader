from enum import Enum

class Validity(Enum):
    INVALID = 0
    VALID = 1
    UNKNOWN = 3

class VDIFHeaderField:
    def __init__(self, name, value, raw_value, validity):
        self._name = name
        self.value = value
        self.raw_value = raw_value
        self._validity = validity

    def _create_for(key, value, raw_value):
        header_field = VDIFHeaderField(
            key, 
            value, 
            raw_value, 
            Validity.UNKNOWN
        )
        return header_field

    def __repr__(self):
        return

    def __str__(self):
        return