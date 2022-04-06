from vdifheader.__utils__ import _warn, _error, _print

def get_first_header(input_filepath):
    '''Returns first header from file at (input_filepath)'''
    headers = get_headers(file_path, count=1)
    if len(headers) != 1:
        _error(f"get_first_header got {len(headers)} results, expected 1.")
        return None
    return headers[0]

def get_headers(input_filepath, count=None):
    '''Returns list of first (count) headers from file at (input_filepath)'''
    header_limit = False
    if count is not None and count > 0:
        header_limit = True
    with open(input_filepath, 'rb') as input_file: