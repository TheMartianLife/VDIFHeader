import pytest
from sys import path
from vdifheader._utils import sanitized_path

HEADER_BYTES = 32


# test that path reconcilliation is working
# TODO
# def test_init_test_sanitized_path():
#     sanitized_path()

# test that the expected test file is present

def test_init_test_file_exists(test_file):
    assert path.isfile(test_file)


# # test internal core of get_headers() function

def test_init_internal_parse_header(test_file):
    header = None
    with open(test_file, "rb") as input_file:
        raw_header = input_file.read(HEADER_BYTES)
        assert len(raw_header) == HEADER_BYTES
    assert header is not None, "VDIFHeader.parse() returned None"

# test utils functions before start of other tests

# TODO
    