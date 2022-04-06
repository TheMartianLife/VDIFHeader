from math import pow

from vdifheader.vdifheaderfield import VDIFHeaderField

def __parse(header):
    word = 0  ### WORD 0
    value, raw_value = header.__get_bits(word, 31)
    __set(header, 'invalid_flag', (value == 1), raw_value)
    value, raw_value = header.__get_bits(word, 30)
    __set(header, 'legacy_mode', (value == 1), raw_value)
    __set(header, 'seconds_from_epoch', *header.__get_bits(word, 0, 29))
    word += 1 ### WORD 1
    __set(header, 'unnassigned_field', *header.__get_bits(word, 30, 31))
    value, raw_value = header.__get_bits(word, 24, 29)
    # TODO transform
    __set(header, 'reference_epoch', value, raw_value)
    __set(header, 'data_frame_number', *header.__get_bits(word, 0, 23))
    word += 1 ### WORD 2
    __set(header, 'vdif_version', *header.__get_bits(word, 29, 31))
    value, raw_value = header.__get_bits(word, 24, 28)
    __set(header, 'num_channels', pow(2, value), raw_value)
    value, raw_value = header.__get_bits(word, 0, 23)
    __set(header, 'data_frame_length', value * 8, raw_value)
    word += 1 ### WORD 3
    value, raw_value = header.__get_bits(word, 31)
    value = ('complex' if value == 1 else 'real')
    __set(header, 'data_type', value, raw_value)
    value, raw_value = header.__get_bits(word, 26, 30)
    __set(header, 'bits_per_sample', value + 1, raw_value)
    __set(header, 'thread_id', *header.__get_bits(word, 16, 25))
    value, raw_value = header.__get_bits(word, 0, 15)
    # TODO transform
    __set(header, 'station_id', value, raw_value)
    word += 1 ### WORD 4
    __set(header, 'extended_data_version', *header.__get_bits(word, 24, 31))
    __set(header, '_extended_data', *header.__get_edv_bits())

def __validate(h):
    h.__assert('invalid_flag', lambda x: x == False, 'invalid_flag is set')
    # legacy mode
    # seconds from epoch
    h.__assert('unnassigned_field', lambda x: x == 0)
    # reference epoch
    # data_frame_number
    h.__assert('vdif_version', lambda x: x >= 0 and x < 2)
    # num channels
    # data frame length
    # TODO all the validation

def __set(header, key, value, raw_value):
    field_object = VDIFHeaderField.__create_for(key, value, raw_value)
    header.setattr(key, field_object)
