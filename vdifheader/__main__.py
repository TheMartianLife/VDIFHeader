from os import path
from sys import argv
from enum import EnumMeta

from vdifheader.__init__ import *

class _VDIFPrintMode(EnumMeta):
    NONE = 0
    SUMMARY = 1
    VALUES = 2
    RAW = 3
    VERBOSE = 4
    def __getitem__(cls, name):
        try:
            return super().__getitem__(name)
        except (KeyError) as error:
            vdifh_warn(f"{name} invalid for print_mode, defaulting to SUMMARY.")
            return _VDIFPrintMode.SUMMARY

def main():
    args = __parse_args(argv[1:])
    if 'show_help' in args:
        __show_help()
        exit(0)
    elif 'input_filepath' not in args:
        # nothing we can do then (shrug)
        __show_usage()
        return

    num_headers = args['num_headers']
    print_mode = args['print_mode']
    input_filepath = args['input_filepath']

    headers = []
    first_header = None
    if num_headers == 1:
        headers = [get_first_header(input_filepath)]
    else:
        headers = get_headers(input_filepath, count=num_headers)

    # make it so if this was launched in -i mode, the headers and first_header
    # variables hold the relevant values
    if len(headers) > 0:
        first_header = headers[0]

    for header in headers:
        if print_mode == _VDIFPrintMode.SUMMARY:
            header.print_summary()
        elif print_mode == _VDIFPrintMode.VALUES:
            header.print_values()
        elif print_mode == _VDIFPrintMode.RAW:
            header.print_raw()
        elif print_mode == _VDIFPrintMode.VERBOSE:
            header.print_verbose()

    print('Done.')

def __parse_args(args):
    parsed_args = { # default values
        'num_headers': -1,
        'print_mode': _VDIFPrintMode.SUMMARY,
        'invalid': []
    }
    value_field = ''
    for arg in args:
        if arg == '-h' or args == '--help':
            parsed_args['show_help'] = True
            return parsed_args
        elif arg == '-n' or arg == 'count':
            value_field = 'num_headers'
        elif arg == '-a' or arg == '--all':
            parsed_args['num_headers'] = -1 # (treated as 'all' value)
        elif arg == '-v' or arg == '--verbose':
            parsed_args['print_mode'] = _VDIFPrintMode.VERBOSE
        elif arg == '-s' or arg == '--silent':
            parsed_args['print_mode'] = _VDIFPrintMode.NONE
        elif arg == '-p' or arg == '--print':
            value_field = 'print_mode'
        elif value_field == 'num_headers':
            try:
                num_headers = int(arg)
            except ValueError:
                parsed_args['invalid'].append(arg)
                vdifh_warn(f"{arg} invalid for num_headers, defaulting to --all.")
                num_headers = -1
            parsed_args['num_headers'] = num_headers
        elif value_field == 'print_mode':
            print_mode_string = arg.upper()
            parsed_args['print_mode'] = _VDIFPrintMode(print_mode_string)
        elif arg == args[-1] and value_field == '':
            parsed_args['input_filepath'] = arg
        else:
            parsed_args['invalid'].append(arg)
            vdifh_warn("{arg} is invalid arg.")
        value_field = ''
    # if we get to here without a valid input_filepath
    if not 'input_filepath' in parsed_args:
        vdifh_error(f"no input_filepath provided.")
    elif not path.isfile(parsed_args['input_filepath']):
        vdifh_error(f"{parsed_args['input_filepath']} is not a file.")
        del parsed_args['input_filepath']
    return parsed_args

def __show_usage():
    vdifh_print('usage: vdifheader [options] [file]')
    return

def __show_help():
    __show_usage()
    vdifh_print('  options:')
    vdifh_print('    -h, --help\t\tshow help')
    vdifh_print('    -n --count [number]\tnumber of headers to parse (default=1)')
    vdifh_print('    -a --all\t\tparse all headers in file')
    vdifh_print('    -v --verbose\tshow all output')
    vdifh_print('    -s --silent\t\tshow minimal output')
    vdifh_print('    -p --print [mode]\tlevel of output to show' \
        '{none|summary|values|raw|verbose}')
    return

if __name__ == '__main__': main()