# > vdifheader - __init__.py
# Defines publicly acessible API functions for the vdifheader package

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
> vdifheader - __init__.py (private)
Defines publicly acessible API functions for the vdifheader package
"""
__all__ = ["vdifheader", "vdifheaderfield"]
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
from sys import stderr
from typing import Optional

from vdifheader.vdifheader import VDIFHeader
from vdifheader.vdifheaderfield import VDIFHeaderField
from vdifheader._utils import Validity

# TODO double-check import access modifiers (private modules are private, etc.)

VDIF_HEADER_BYTES = 32
STATION_ID_FILE = "station_ids.csv"


def get_first_header(input_filepath: str) -> Optional[VDIFHeader]:
    """
    Returns first header from file at input filepath

        parameter:
            input_filepath: str     path to a valid VDIF file

        returns:
            Optional[VDIFHeader]    header data if found, else None
    """
    # just call get_headers but with count=1
    headers = list(get_headers(input_filepath, count=1))
    # then make sure there was one result, and extract it from the result array
    if len(headers) != 1:
        stderr.write(f"get_first_header found {len(headers)} headers, " \
            "expected 1.\n")
        return None
    return headers[0]


def get_headers(input_filepath: str, 
        count: Optional[int]=None) -> list[VDIFHeader]:
    """
    Returns list of first count headers from file at input filepath

        parameter:
            input_filepath: str     the path to a valid VDIF file
            count: Optional[int]    number of headers to parse, else parse all

        returns:
           list[VDIFHeader]         header data if found, else empty    
    """
    header_limit = False
    # if count is invalid, header_limit is disabled. include all headers in file
    if count is not None and count > 0:
        header_limit = True
    parsed_count = 0
    header_num = None # set by (and then relative to) first header
    # allow relative/home-relative filepaths
    input_realpath = path.realpath(path.expanduser(input_filepath))
    with open(input_realpath, "rb") as input_file:
        raw_header = input_file.read(VDIF_HEADER_BYTES)
        # until we find the end of the file, or otherwise break
        while raw_header is not None and len(raw_header) > 0:
            # parse the fetched raw header bytes
            if parsed_count == 0:
                header = VDIFHeader.parse(raw_header)
                # set start value for expected data frame numbers
                header_num = header.header_num
            else:
                header = VDIFHeader.parse(raw_header, header_num + parsed_count)
            yield header
            parsed_count += 1
            # check if we've found as many headers as asked for
            if header_limit and parsed_count == count:
                break
            # otherwise scrub past raw frame bytes
            seek_length = header.data_frame_length.value - VDIF_HEADER_BYTES
            input_file.seek(seek_length, 1)  # 1 = relative to current position
            # and get next raw header bytes
            raw_header = input_file.read(VDIF_HEADER_BYTES)
    if header_limit and parsed_count != count:
        stderr.write(f"get_headers found {parsed_count} headers, expected " \
            "{count}.\n")
