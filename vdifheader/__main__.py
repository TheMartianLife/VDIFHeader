# > vdifheader - __main__.py
# Defines argument parser and main methods for package run in script mode

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
Defines argument parser and main methods for package run in script mode
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

import sys
from enum import Enum
from argparse import ArgumentParser

from vdifheader import *
from vdifheader._utils import *


class VDIFOutputMode(Enum):
    VALUES = "values"
    BINARY = "binary"


def arg_parser() -> ArgumentParser:
    # parse command line args
    parser = ArgumentParser(prog="vdifheader", 
        description="Parse and validate VDIF headers")
    # arguments about number of headers to parse
    num_group = parser.add_mutually_exclusive_group()
    num_group.add_argument("-n", "--count", dest="num_headers", 
        metavar="NUM", type=posint, help="number of headers to parse")
    num_group.add_argument("-a", "--all", dest="num_headers", 
        action="store_const", const=-1, help="parse all headers in file")
    # arguments about how to print output
    print_group = parser.add_mutually_exclusive_group()
    print_group.add_argument("-v", "--values", dest="output_mode", 
        action="store_const", const=VDIFOutputMode.VALUES, 
        help="show values output")
    print_group.add_argument("-b", "--binary", dest="output_mode", 
        action="store_const", const=VDIFOutputMode.BINARY, 
        help="show raw binary output")
    # arguments about file to process
    parser.add_argument("input_file", metavar="INPUT_FILE", type=filepath)
    parser.set_defaults(num_headers=1, output_mode=VDIFOutputMode.VALUES)
    return parser


def main():
    """Gets headers from input filepath and prints output in requested mode"""
    # global variables for access in interactive mode after main() completes
    global headers
    global first_header
    headers = []
    first_header = None

    # parse command line args
    args = vars(arg_parser().parse_args())

    num_headers = args["num_headers"]
    output_mode = args["output_mode"]
    input_file = args["input_file"]

    for header in get_headers(input_file, count=num_headers):
        # save first header if this is it
        if first_header is None:
            first_header = header
        # show requested output
        if output_mode == VDIFOutputMode.VALUES:
            header.print_values()
        elif output_mode == VDIFOutputMode.BINARY:
            header.print_binary()
        # print a blank line between separate headers
        if num_headers > 1:
            print()
    return


if __name__ == "__main__":
    main()
