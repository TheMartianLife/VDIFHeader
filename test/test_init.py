import pytest
from os import path

import vdifheader as vh
from vdifheader._utils import sanitized_path

HEADER_BYTES = 32

# test that path reconcilliation is working
# test that the expected test file is present
# test internal core of get_headers() function
# test finding of first header within files
# test finding of headers within files


# test that the expected test file is present

@pytest.mark.fast
def test_init_test_file_exists(test_file):
    assert path.isfile(test_file)


# test internal core of get_headers() function

@pytest.mark.fast
def test_init_internal_parse_header(test_file):
    header = None
    with open(sanitized_path(test_file), "rb") as input_file:
        raw_header = input_file.read(HEADER_BYTES)
        assert len(raw_header) == HEADER_BYTES
        header = vh.VDIFHeader.parse(raw_header)
    assert header is not None, "VDIFHeader.parse() returned None"

# test finding of first header within files

@pytest.mark.fast
def test_init_get_first_header(test_file):
    first_header = vh.get_first_header(test_file)
    assert first_header is not None


# test finding of headers within files

@pytest.mark.slow
@pytest.mark.parametrize("count, result_count", [
    (1, 1), 
    (5, 5), 
    (1000000,30000), 
    (-1, 30000)])
def test_init_get_headers(test_file, count, result_count):
    first_header = vh.get_first_header(test_file)
    headers = []
    for header in vh.get_headers("./test.vdif", count=count):
        headers.append(header)
    assert len(headers) == result_count
    assert first_header == headers[0]
