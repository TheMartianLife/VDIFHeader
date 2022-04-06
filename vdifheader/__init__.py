from vdifheader.__utils__ import __warn, __error, __print
from vdifheader.__parser__ import parse

from vdifheader.vdifheader import VDIFHeader

HEADER_BYTES = 32

def get_first_header(input_filepath):
    '''Returns first header from file at (input_filepath)'''
    headers = get_headers(input_filepath, count=1)
    if len(headers) != 1:
        __error(f"get_first_header got {len(headers)} results, expected 1.")
        return None
    return headers[0]

def get_headers(input_filepath, count=None):
    '''Returns list of first (count) headers from file at (input_filepath)'''
    header_limit = False
    if count is not None and count > 0:
        header_limit = True
    parsed_count = 0
    with open(input_filepath, 'rb') as input_file:
        raw_header = input_file.read(HEADER_BYTES)
        header = VDIFHeader.parse(raw_header, parsed_count)
        yield header
        parsed_count += 1
        input_file.seek(header.data_frame_length -HEADER_BYTES)
    if parsed_count == 0:
        __error('get_headers failed to read data.')
    elif header_limit and parsed_count != count:
        __warn(f"get_headers found {parsed_count} headers, expected {count}.")

def vdifh_warn(message): 
    return __warn(message)

def vdifh_error(message): 
    return __error(message)

def vdifh_print(message): 
    return __print(message)