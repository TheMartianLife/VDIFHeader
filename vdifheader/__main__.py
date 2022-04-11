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

from os import path, strerror
from sys import stdout
from errno import ENOENT
from enum import Enum
from argparse import ArgumentParser

from vdifheader.__init__ import *


class VDIFPrintMode(Enum):
    NONE = "none"
    SUMMARY = "summary"
    VALUES = "values"
    RAW = "raw"
    VERBOSE = "verbose"

    def __str__(self):
        return self.value

class VDIFFieldValidity(Enum):
    UNKNOWN = 0
    INVALID = 1
    VALID = 2


def main():
    """Gets headers from input filepath and prints output in requested mode"""
    # global variables for access in interactive mode after main() completes
    global headers
    global first_header
    headers = []
    first_header = None

    # parse command line args
    parser = ArgumentParser(description="Parse and validate VDIF headers")
    # arguments about number of headers to parse
    num_group = parser.add_mutually_exclusive_group()
    num_group.add_argument("-n", "--count", dest="num_headers", 
        metavar="NUM_HEADERS", type=int) # TODO disallow negative numbers
    num_group.add_argument("-a", "--all", dest="num_headers", 
        action="store_const", const=-1)
    # arguments about how to print output
    print_group = parser.add_mutually_exclusive_group()
    print_group.add_argument("-v", "--verbose", dest="print_mode", 
        action="store_const", const=VDIFPrintMode.VERBOSE)
    print_group.add_argument("-s", "--silent", dest="print_mode", 
        action="store_const", const=VDIFPrintMode.NONE)
    print_group.add_argument("-p", "--print", dest="print_mode", 
        metavar="INPUT_FILES", type=VDIFPrintMode, choices=list(VDIFPrintMode))
    # arguments about files to process
    parser.add_argument("input_files", nargs="+") # TODO validate input
    parser.set_defaults(num_headers=1, print_mode=VDIFPrintMode.SUMMARY)




    test_args_string1 = "-n 10 --verbose ~/test_data/m0921_Mp_264_042000.vdif"
    args = parser.parse_args(test_args_string1)
    print(args)

    test_args_string2 = "-n --p empty ../../m0921_Mp_264_042000.vdif"
    args = parser.parse_args(test_args_string2)   
    print(args)

    test_args_string3 = "--all --verbose ../../m0921_Mp_264_04200.vdif"
    args = parser.parse_args(test_args_string3) 
    print(args)

    test_args_string4 = "-n 10 --all --verbose"
    args = parser.parse_args(test_args_string4) 
    print(args)

    # get and validate arguments
    # args = __parse_args(argv[1:])
    # if "show_help" in args:
    #     __show_help()
    #     return
    # elif "input_filepath" not in args:
    #     # nothing we can do then (shrug)
    #     __show_usage()
    #     return

    # num_warnings = 0
    # num_errors = 0

    # # values that should match between headers
    # checks = {
    #     "data_header_lengths": set(),
    #     "data_frame_lengths": set(),
    #     "channel_counts": set(),
    #     "bit_counts": set(),
    #     "station_ids": set(),
    # }

    # get some headers
    # for header in get_headers(args["input_filepath"], args["num_headers"]):
    #     headers.append(header)
    #     # TODO set expected value of supposedly matching fields
    #     if first_header is None:
    #         first_header = header

        # TODO remove
        # header.set_expected_value("station_id", "Tt")
        # header.revalidate()
        # save first header if this is it
        # print requested output about this header
        # __print_header_output(header, args["print_mode"])
        # # add to total warnings and errors from each header
        # num_warnings += header.warnings_count
        # num_errors += header.errors_count
        # check values that should match between headers
        # header_length = 16 if header.legacy_mode else 32
        # checks["data_header_lengths"].add(header_length)
        # checks["data_frame_lengths"].add(header.data_frame_length)
        # checks["channel_counts"].add(header.num_channels)
        # checks["bit_counts"].add(header.bits_per_sample)
        # checks["station_ids"].add(header.station_id)
    # file-wide warnings about non-matching fields between headers
    # for key, value in checks.items():
    #     if len(value) > 1:
    #         message = f"ERROR: value {key} did not match between headers."
    #         stderr.write(colorify(message))
    #         num_errors += 1
    # show total errors and warnings
    # if args["print_mode"] != _VDIFPrintMode.NONE:
    #     stdout.write(f"{num_errors} errors, {num_warnings} warnings " \
    #         "generated.\n")
    # stdout.write(f"Parsed {len(headers)} headers.")
    return

def __check_input_filepath_arg(parser, arg):
    filepath = path.expanduser(arg) # resolve ~ relativity if present
    filepath = path.realpath(filepath) # resolve ./ relativity if present
    filepath = path.normpath(filepath) # compresses any remaining ../ relativity
    if not path.exists(filepath):
        raise FileNotFoundError(ENOENT, strerror(ENOENT), filepath)
    return open(filepath, "rb")


if __name__ == "__main__":
    main()



# def __parse_args(args: list[str]) -> dict[str, Union[int, str, _VDIFPrintMode]]:
    # """Parses and validates args and flags, setting defaults where needed"""
    # parsed_args = {  # default values
    #     "num_headers": -1,
    #     "print_mode": _VDIFPrintMode.SUMMARY,
    #     "invalid": [],
    # }
    # value_field = ""
    # # TODO test and support stringed args and stringed/escaped filepath args
    # for arg in args:
    #     if arg == "-h" or args == "--help":
    #         parsed_args["show_help"] = True
    #         return parsed_args
    #     elif arg == "-n" or arg == "--count":
    #         value_field = "num_headers"
    #     elif arg == "-a" or arg == "--all":
    #         parsed_args["num_headers"] = -1  # (treated as 'all' value)
    #     elif arg == "-v" or arg == "--verbose":
    #         parsed_args["print_mode"] = _VDIFPrintMode.VERBOSE
    #     elif arg == "-s" or arg == "--silent":
    #         parsed_args["print_mode"] = _VDIFPrintMode.NONE
    #     elif arg == "-p" or arg == "--print":
    #         value_field = "print_mode"
    #     elif value_field == "num_headers":
    #         try:
    #             num_headers = int(arg)
    #         except ValueError:
    #             parsed_args["invalid"].append(f"-n {arg}")
    #             stderr.write(f"WARNING: arg {arg} invalid for num_headers. " \
    #                 "Defaulting to all.\n")
    #             num_headers = -1
    #         parsed_args["num_headers"] = num_headers
    #         value_field = ""
    #     elif value_field == "print_mode":
    #         try:
    #             print_mode = _VDIFPrintMode[arg.upper()]
    #         except KeyError:
    #             parsed_args["invalid"].append(f"-p {arg}")
    #             stderr.write(f"WARNING: arg '{arg}' invalid for print_mode. " \
    #                 "Defaulting to 'summary'.\n")
    #             print_mode = _VDIFPrintMode.SUMMARY
    #         parsed_args["print_mode"] = print_mode
    #         value_field = ""
    #     elif arg == args[-1] and value_field == "":
    #         parsed_args["input_filepath"] = arg
    #     else:
    #         parsed_args["invalid"].append(arg)
    #         stderr.write(f"WARNING: arg {arg} is invalid arg for position. " \
    #             "Ignoring arg.\n")
    # # if we get to here without a valid input_filepath
    # if not "input_filepath" in parsed_args:
    #     stderr.write(f"ERROR: no input_filepath provided.\n")
    # elif not path.isfile(parsed_args["input_filepath"]):
    #     stderr.write(f"ERROR: {parsed_args['input_filepath']} is not a " \
    #         "file.\n")
    #     del parsed_args["input_filepath"] # invalid is as good as none
    # return parsed_args


# def __print_header_output(header: VDIFHeader, print_mode: _VDIFPrintMode):
#     """Prints the specified level of output information about given header"""
#     # if print_mode == _VDIFPrintMode.SUMMARY:
#     #     header.print_summary()
#     # el
#     if print_mode == _VDIFPrintMode.VALUES:
#         header.print_values()
#         stdout.write("\n")
#     elif print_mode == _VDIFPrintMode.RAW:
#         header.print_raw()
#         stdout.write("\n")
#     elif print_mode == _VDIFPrintMode.VERBOSE:
#         header.print_verbose()
#         stdout.write("\n")
#     return


# def __show_usage():
#     """Shows one-line usage information"""
#     stdout.write("usage: vdifheader [options] [file]\n")
#     return


# def __show_help():
#     """Shows a nicely styled manpage-like description of valid args and flags"""
#     __show_usage() # show usage line first
#     stdout.write("  options:\n")
#     stdout.write("    -h, --help\t\tshow help\n")
#     stdout.write("    -n --count [arg]\tnumber of headers to parse " \
#         "(default=1)\n")
#     stdout.write("    -a --all\t\tparse all headers in file\n")
#     stdout.write("    -v --verbose\tshow all output\n")
#     stdout.write("    -s --silent\t\tshow minimal output\n")
#     stdout.write("    -p --print [arg]\tlevel of output to show" \
#         "{none|summary|values|raw|verbose} (default=summary)\n")
#     return
