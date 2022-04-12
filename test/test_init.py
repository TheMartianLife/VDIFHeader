import os, pytest
from vdifheader import *

HEADER_BYTES = 32

# test that path reconcilliation is working
# test that the expected test file is present
# test internal core of get_headers() method
# test finding of first header within files
# test finding of headers within files


# test that the expected test file is present

@pytest.mark.fast
def test_init_test_file_exists(test_filepath):
    assert os.path.isfile(test_filepath)


# test internal core of get_headers method

@pytest.mark.fast
def test_init_internal_parse_header(test_filepath):
    header = None
    with open(test_filepath, "rb") as input_file:
        raw_header = input_file.read(HEADER_BYTES)
        assert len(raw_header) == HEADER_BYTES
        header = VDIFHeader.parse(raw_header)
    assert header is not None, "VDIFHeader.parse() returned None"

# test finding of first header within files

@pytest.mark.fast
def test_init_get_first_header(test_filepath):
    first_header = get_first_header(test_filepath)
    assert first_header is not None


# test finding of headers within files

@pytest.mark.slow
@pytest.mark.parametrize("count, result_count", [
    (1, 1), 
    (5, 5), 
    (1000000,30000), 
    (-1, 30000)])
def test_init_get_headers(test_filepath, count, result_count):
    first_header = get_first_header(test_filepath)
    headers = []
    for header in get_headers("./test.vdif", count=count):
        headers.append(header)
    assert len(headers) == result_count
    assert first_header == headers[0]
