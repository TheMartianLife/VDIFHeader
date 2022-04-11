import pytest
from os import path
from copy import deepcopy
from vdifheader import VDIFHeader as Header
from vdifheader import VDIFHeaderField as Field
pytestmark = pytest.mark.fast

# test that header object can't be instantiated directly
# test that value-wise equality between objects is enabled
# test that raw data preprocessing is producing expected output
# test that decode/encode and get/set of each field is working as expected
# test that print output looks as expected

@pytest.fixture(scope="module")
def cached_header():
    header = None
    with open(path.abspath("./test.vdif"), "rb") as input_file:
        raw_header = input_file.read(32)
        header = Header.parse(raw_header)
    assert header is not None
    return header


# test that header object can't be instantiated directly

def test_vdifheader_init():
    header = None
    with pytest.raises(NotImplementedError):
        header = Header()
    assert header == None


# test that value-wise equality between objects is enabled

def test_vdifheader_eq(cached_header):
    other_header = deepcopy(cached_header)
    assert other_header is not cached_header
    assert cached_header == other_header


# test that raw data preprocessing is producing expected output

def test_vdifheader_preprocess():
    preprocessed_bits = ""
    with open(path.abspath("./test.vdif"), "rb") as input_file:
        raw_data = input_file.read(32)
        preprocessed_bits = Header._preprocess(raw_data)
    raw_bits = "00001111111010100011011000000000" \
        "00000000000000000000000011010100" \
        "00110111110000000000000010000000" \
        "00101110001010100000000000100000" \
        "00000000000000000000000000000000" \
        "00000000000000000000000000000000" \
        "00000000000000000000000000000000" \
        "00000000000000000000000000000000"
    assert preprocessed_bits == raw_bits, "Header.preprocess() has " \
        "produced incorrect binary output"


# test that decode/encode and get/set of each field is working as expected

@pytest.mark.parametrize("value, raw_value", [(True, "1"), (False, "0")])
def test_vdifheader_invalid_flag_assignment(cached_header, value, raw_value):
    cached_header.invalid_flag = value
    assert cached_header.invalid_flag == value
    assert cached_header._get_raw_value(Field.INVALID_FLAG) == raw_value

def test_vdifheader_legacy_mode(cached_header):
    assert cached_header.legacy_mode == False


@pytest.mark.parametrize("value, raw_value", [(True, "1"), (False, "0")])
def test_vdifheader_legacy_mode_assignment(cached_header, value, raw_value):
    cached_header.legacy_mode = value
    assert cached_header.legacy_mode == value
    assert cached_header._get_raw_value(Field.LEGACY_MODE) == raw_value   


def test_vdifheader_seconds_from_epoch(cached_header):
    assert cached_header.seconds_from_epoch == 7100400

# def test_vdifheader_seconds_from_epoch_assignment(cached_header, value, raw_value):
    # TODO


def test_vdifheader_unassigned_field(cached_header):
    assert cached_header.unassigned_field == 0

@pytest.mark.parametrize("value, raw_value", [(0, "00")])
def test_vdifheader_unassigned_field_assignment(cached_header, value, raw_value):
    cached_header.unassigned_field = value
    _raw_value = "".join(reversed(raw_value))
    assert cached_header.unassigned_field == value
    assert cached_header._get_raw_value(Field.UNASSIGNED_FIELD) == _raw_value

@pytest.mark.parametrize("value", [4, -1])
def test_vdifheader_unassigned_field_assignment_invalid(cached_header, value):
    initial_value = cached_header.unassigned_field
    inital_raw_value = cached_header._get_raw_value(Field.UNASSIGNED_FIELD)
    with pytest.raises(ValueError):
        cached_header.unassigned_field = value
    assert cached_header.unassigned_field == initial_value
    assert cached_header._get_raw_value(Field.UNASSIGNED_FIELD) == inital_raw_value  

@pytest.mark.parametrize("value, raw_value", [(1, "01"), (2, "10"), (3, "11")])
def test_vdifheader_unassigned_field_assignment_warning(cached_header, value, raw_value):
    cached_header.unassigned_field = value
    _raw_value = "".join(reversed(raw_value))
    assert cached_header.unassigned_field == value
    assert cached_header._get_raw_value(Field.UNASSIGNED_FIELD) == _raw_value
    # TODO re-include after pytest issue #5997 is addressed
    # https://github.com/pytest-dev/pytest/issues/5997
    # _stderr = capsys.readouterr().err
    # assert f"WARNING: extended_data_version {value} not recognised." in _stderr


# def test_vdifheader_reference_epoch(cached_header): # TODO "2021-07-01"
    # TODO

# def test_vdifheader_reference_epoch_assignment(cached_header, value, raw_value):
    # TODO


def test_vdifheader_data_frame_number(cached_header):
    assert cached_header.data_frame_number == 0

@pytest.mark.parametrize("value, raw_value", [
    (1023,  "000000000000001111111111"), 
    (500,   "000000000000000111110100"),
    (0, "000000000000000000000000")])
def test_vdifheader_data_frame_number_assignment(cached_header, value, raw_value):
    cached_header.data_frame_number = value
    _raw_value = "".join(reversed(raw_value))
    assert cached_header.data_frame_number == value
    assert cached_header._get_raw_value(Field.DATA_FRAME_NUMBER) == _raw_value

@pytest.mark.parametrize("value", [16777216, -1])
def test_vdifheader_data_frame_number_assignment_invalid(cached_header, value):
    initial_value = cached_header.data_frame_number
    inital_raw_value = cached_header._get_raw_value(Field.DATA_FRAME_NUMBER)
    with pytest.raises(ValueError):
        cached_header.data_frame_number = value
    assert cached_header.data_frame_number == initial_value
    assert cached_header._get_raw_value(Field.DATA_FRAME_NUMBER) == inital_raw_value  


def test_vdifheader_vdif_version(cached_header):
    assert cached_header.vdif_version == 0

# def test_vdifheader_vdif_version_assignment(cached_header, value, raw_value):
    # TODO


def test_vdifheader_num_channels(cached_header):
    assert cached_header.num_channels == 2

# def test_vdifheader_num_channels_assignment(cached_header, value, raw_value):
    # TODO


def test_vdifheader_data_frame_length(cached_header):
    assert cached_header.data_frame_length == 8032

# def test_vdifheader_data_frame_length_assignment(cached_header, value, raw_value):
    # TODO


def test_vdifheader_data_type(cached_header):
    assert cached_header.data_type == "real"

@pytest.mark.parametrize("value, raw_value", [("complex", "1"), ("real", "0")])
def test_vdifheader_data_type_assignment(cached_header, value, raw_value):
    cached_header.data_type = value
    assert cached_header.data_type == value
    assert cached_header._get_raw_value(Field.DATA_TYPE) == raw_value   


def test_vdifheader_bits_per_sample(cached_header):
    assert cached_header.bits_per_sample == 2

# def test_vdifheader_bits_per_sample_assignment(cached_header, value, raw_value):
    # TODO


def test_vdifheader_thread_id(cached_header):
    assert cached_header.thread_id == 0

# def test_vdifheader_thread_id_assignment(cached_header, value, raw_value):
    # TODO


def test_vdifheader_station_id(cached_header):
    assert cached_header.station_id == "Tt"

@pytest.mark.parametrize("value, raw_value", [
    ("Mp", "0111000001001101"),
    ("125", "0000000001111101"),
    ("16", "0000000000010000")])
def test_vdifheader_station_id_assignment(cached_header, value, raw_value):
    cached_header.station_id = value
    _raw_value = "".join(reversed(raw_value))
    assert cached_header.station_id == value
    assert cached_header._get_raw_value(Field.STATION_ID) == _raw_value


def test_vdifheader_extended_data_version(cached_header):
    assert cached_header.extended_data_version == 0

@pytest.mark.parametrize("value, raw_value",[
    (0x00, "00000000"),
    (0x01, "00000001"),
    (0x02, "00000010"),
    (0x03, "00000011"),
    (0x04, "00000100"),
])
def test_vdifheader_extended_data_version_assignment(cached_header, value, raw_value):
    cached_header.extended_data_version = value
    _raw_value = "".join(reversed(raw_value))
    assert cached_header.extended_data_version == value
    assert cached_header._get_raw_value(Field.EXTENDED_DATA_VERSION) == _raw_value  

@pytest.mark.parametrize("value", [256, -1])
def test_vdifheader_extended_data_version_assignment_invalid(cached_header, value):
    initial_value = cached_header.extended_data_version
    inital_raw_value = cached_header._get_raw_value(Field.EXTENDED_DATA_VERSION)
    with pytest.raises(ValueError):
        cached_header.extended_data_version = value
    assert cached_header.extended_data_version == initial_value
    assert cached_header._get_raw_value(Field.EXTENDED_DATA_VERSION) == inital_raw_value  

@pytest.mark.parametrize("value, raw_value", [(0x05, "00000101")])
def test_vdifheader_extended_data_version_assignment_warning(cached_header, value, raw_value, capsys):
    cached_header.extended_data_version = value
    _raw_value = "".join(reversed(raw_value))
    assert cached_header.extended_data_version == value
    assert cached_header._get_raw_value(Field.EXTENDED_DATA_VERSION) == _raw_value
    # TODO re-include after pytest issue #5997 is addressed
    # https://github.com/pytest-dev/pytest/issues/5997
    # _stderr = capsys.readouterr().err
    # assert f"WARNING: extended_data_version {value} not recognised." in _stderr


def test_vdifheader_extended_data(cached_header): 
    assert cached_header.extended_data == {}

# def test_vdifheader_extended_data_assignment(cached_header, value, raw_value):
# TODO


# test that print output looks as expected

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
    # TODO re-include after pytest issue #5997 is addressed
    # https://github.com/pytest-dev/pytest/issues/5997
    # _stdout = capsys.readouterr().out
    # assert _stdout == "\n".join(output) 

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
    # TODO re-include after pytest issue #5997 is addressed
    # https://github.com/pytest-dev/pytest/issues/5997
    # _stdout = capsys.readouterr().out
    # assert _stdout == "\n".join(output)