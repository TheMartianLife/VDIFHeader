# > vdifheader - __main__.py
# Defines argument parser and main functions for package run in script mode

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
> vdifheader - __main__.py (private)
Defines argument parser and main functions for package run in script mode
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

from os import path
from sys import argv, stderr, stdout
from enum import Enum

from vdifheader.__init__ import *


class _VDIFPrintMode(Enum):
    NONE = 0
    SUMMARY = 1
    VALUES = 2
    RAW = 3
    VERBOSE = 4


def main():
    """Gets headers from input filepath and prints output in requested mode"""
    # global variables for access in interactive mode after main() completes
    global headers
    global first_header
    headers = []
    first_header = None

    # get and validate arguments
    args = __parse_args(argv[1:])
    if "show_help" in args:
        __show_help()
        return
    elif "input_filepath" not in args:
        # nothing we can do then (shrug)
        __show_usage()
        return

    num_headers = args["num_headers"]
    print_mode = args["print_mode"]
    input_filepath = args["input_filepath"]

    if num_headers == 1:
        headers = [get_first_header(input_filepath)]
    else:
        headers = list(get_headers(input_filepath, count=num_headers))

    # make it so if this was launched in -i mode, the headers and first_header
    # variables hold the relevant values
    if len(headers) > 0:
        first_header = headers[0]

    num_warnings = 0
    num_errors = 0
    divider = str("=" * 72) + "\n"
    for header in headers:
        # print requested output
        if print_mode == _VDIFPrintMode.SUMMARY:
            header.print_summary()
        elif print_mode == _VDIFPrintMode.VALUES:
            header.print_values()
            stdout.write(divider)
        elif print_mode == _VDIFPrintMode.RAW:
            header.print_raw()
            stdout.write(divider)
        elif print_mode == _VDIFPrintMode.VERBOSE:
            header.print_verbose()
            stdout.write(divider)
        # total the warnings and errors from each header
        num_warnings += header.warnings_count
        num_errors += header.errors_count
    if print_mode != _VDIFPrintMode.NONE:
        stdout.write(f"{num_errors} errors, {num_warnings} warnings " \
            "generated.\n")
    return


def __parse_args(args):
    """Parses and validates args and flags, setting defaults where needed"""
    parsed_args = {  # default values
        "num_headers": -1,
        "print_mode": _VDIFPrintMode.SUMMARY,
        "invalid": [],
    }
    value_field = ""
    for arg in args:
        if arg == "-h" or args == "--help":
            parsed_args["show_help"] = True
            return parsed_args
        elif arg == "-n" or arg == "count":
            value_field = "num_headers"
        elif arg == "-a" or arg == "--all":
            parsed_args["num_headers"] = -1  # (treated as 'all' value)
        elif arg == "-v" or arg == "--verbose":
            parsed_args["print_mode"] = _VDIFPrintMode.VERBOSE
        elif arg == "-s" or arg == "--silent":
            parsed_args["print_mode"] = _VDIFPrintMode.NONE
        elif arg == "-p" or arg == "--print":
            value_field = "print_mode"
        elif value_field == "num_headers":
            try:
                num_headers = int(arg)
            except ValueError:
                parsed_args["invalid"].append(f"-n {arg}")
                stderr.write(f"WARNING: arg {arg} invalid for num_headers. " \
                    "Defaulting to all.\n")
                num_headers = -1
            parsed_args["num_headers"] = num_headers
            value_field = ""
        elif value_field == "print_mode":
            try:
                print_mode = _VDIFPrintMode[arg.upper()]
            except KeyError:
                parsed_args["invalid"].append(f"-p {arg}")
                stderr.write(f"WARNING: arg '{arg}' invalid for print_mode. " \
                    "Defaulting to 'summary'.\n")
                print_mode = _VDIFPrintMode.SUMMARY
            parsed_args["print_mode"] = print_mode
            value_field = ""
        elif arg == args[-1] and value_field == "":
            parsed_args["input_filepath"] = arg
        else:
            parsed_args["invalid"].append(arg)
            stderr.write(f"WARNING: arg {arg} is invalid arg for position. " \
                "Ignoring arg.\n")
    # if we get to here without a valid input_filepath
    if not "input_filepath" in parsed_args:
        stderr.write(f"ERROR: no input_filepath provided.\n")
    elif not path.isfile(parsed_args["input_filepath"]):
        stderr.write(f"ERROR: {parsed_args['input_filepath']} is not a " \
            "file.\n")
        del parsed_args["input_filepath"] # invalid is as good as none
    return parsed_args


def __show_usage():
    """Shows one-line usage information"""
    stdout.write("usage: vdifheader [options] [file]\n")
    return


def __show_help():
    """Shows a nicely styled manpage-like description of valid args and flags"""
    __show_usage() # show usage line first
    stdout.write("  options:\n")
    stdout.write("    -h, --help\t\tshow help\n")
    stdout.write("    -n --count [arg]\tnumber of headers to parse\n")
    stdout.write("    -a --all\t\tparse all headers in file (default)\n")
    stdout.write("    -v --verbose\tshow all output\n")
    stdout.write("    -s --silent\t\tshow minimal output\n")
    stdout.write(
        "    -p --print [arg]\tlevel of output to show"
        "{none|summary|values|raw|verbose}\n"
    )
    return


if __name__ == "__main__":
    main()
