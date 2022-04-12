import os, pytest
from copy import deepcopy
from vdifheader import VDIFHeader
pytestmark = pytest.mark.fast

# test that header object can't be instantiated directly
# test that value-wise equality between objects is enabled
# test that raw data preprocessing is producing expected output
# test that decode/encode and get/set of each field is working as expected
# test that print output looks as expected

# test that header object can't be instantiated directly

def test_vdifheader_init():
    header = None
    with pytest.raises(NotImplementedError):
        header = VDIFHeader()
    assert header == None


# test that value-wise equality between objects is enabled

def test_vdifheader_eq(cached_header):
    other_header = deepcopy(cached_header)
    assert other_header is not cached_header
    assert cached_header == other_header


# test that raw data preprocessing is producing expected output

def test_vdifheader_preprocess(test_filepath):
    preprocessed_bits = ""
    with open(test_filepath, "rb") as input_file:
        raw_data = input_file.read(32)
        preprocessed_bits = VDIFHeader._preprocess(raw_data)
    raw_bits = "00001111111010100011011000000000" \
        "00000000000000000000000011010100" \
        "00110111110000000000000010000000" \
        "00101110001010100000000000100000" \
        "00000000000000000000000000000000" \
        "00000000000000000000000000000000" \
        "00000000000000000000000000000000" \
        "00000000000000000000000000000000"
    assert preprocessed_bits == raw_bits


# test that print output looks as expected

@pytest.mark.skipif(os.environ.get("CAPSYS_WORKING") != "True",
    reason="capsys capture of stdout not working in current pytest")
def test_vdifheader_print_values(cached_header, capsys):
    output = ["Invalid flag: False",
        "Legacy mode: False",
        "Time from epoch: 7100400 seconds",
        "Reference epoch: 2021-07-01 00:00:00+00:00 UTC",
        "Data frame number: 0",
        "VDIF version: 0",
        "Number of channels: 2.0",
        "Data frame length: 8032 bytes",
        "Data type: real",
        "Bits per sample: 2 bit(s)",
        "Thread ID: 0",
        "Station ID: Tt",
        "Extended data version: 0"]
    cached_header.print_values()
    _stdout = capsys.readouterr().out
    assert _stdout == "\n".join(output) 

@pytest.mark.skipif(os.environ.get("CAPSYS_WORKING") != "True",
    reason="capsys capture of stdout not working in current pytest")
def test_vdifheader_print_raw(cached_header, capsys):
    output = ["       |     Byte 3    |     Byte 2    |     Byte 1    |     Byte 0    |",
        "Word 0 |0|0|0 0 0 0 1 1 1 1 1 1 1 0 1 0 1 0 0 0 1 1 0 1 1 0 0 0 0 0 0 0|",
        "Word 1 |0 0|1 1 0 1 0 1|0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0|",
        "Word 2 |0 0 0|1 0 0 0 0|0 0 1 1 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0|",
        "Word 3 |0|1 0 0 0 0|0 0 0 0 0 0 0 0 0 0|0 0 1 0 1 0 1 0 0 0 1 0 1 1 1 0|",
        "Word 4 |0 0 0 0 0 0 0 0|0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0|",
        "Word 5 |0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0|",
        "Word 6 |0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0|",
        "Word 7 |0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0|"]
    cached_header.print_raw()
    _stdout = capsys.readouterr().out
    assert _stdout == "\n".join(output)