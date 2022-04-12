import os, pytest
from datetime import datetime, timezone
from vdifheader import VDIFHeaderField as Field
from vdifheader._utils import switch_end
pytestmark = pytest.mark.fast

# test that decode/encode and get/set of each field is working as expected


# test invalid_flag field (get, set, attempt set invalid)

def test_vdifheader_invalid_flag(cached_header):
    assert cached_header.invalid_flag == False

@pytest.mark.parametrize("value, raw_value", [(True, "1"), (False, "0")])
def test_vdifheader_invalid_flag_assignment(cached_header, value, raw_value):
    cached_header.invalid_flag = value
    assert cached_header.invalid_flag == value
    assert cached_header._get_raw_value(Field.INVALID_FLAG) == raw_value

@pytest.mark.parametrize("value", [1, 0, "True", "false"])
def test_vdifheader_invalid_flag_assignment_invalid(cached_header, value):
    initial_value = cached_header.invalid_flag
    inital_raw_value = cached_header._get_raw_value(Field.INVALID_FLAG)
    with pytest.raises(TypeError):
        cached_header.invalid_flag = value
    assert cached_header.invalid_flag == initial_value
    assert cached_header._get_raw_value(Field.INVALID_FLAG) == inital_raw_value  


# test legacy_mode field (get, set, attempt set invalid)

def test_vdifheader_legacy_mode(cached_header):
    assert cached_header.legacy_mode == False

@pytest.mark.parametrize("value, raw_value", [(True, "1"), (False, "0")])
def test_vdifheader_legacy_mode_assignment(cached_header, value, raw_value):
    cached_header.legacy_mode = value
    assert cached_header.legacy_mode == value
    assert cached_header._get_raw_value(Field.LEGACY_MODE) == raw_value   

@pytest.mark.parametrize("value", [1, 0, "True", "false"])
def test_vdifheader_legacy_mode_assignment_invalid(cached_header, value):
    initial_value = cached_header.legacy_mode
    inital_raw_value = cached_header._get_raw_value(Field.LEGACY_MODE)
    with pytest.raises(TypeError):
        cached_header.legacy_mode = value
    assert cached_header.legacy_mode == initial_value
    assert cached_header._get_raw_value(Field.LEGACY_MODE) == inital_raw_value  


# test seconds_from_epoch field (get, set, attempt set invalid)

def test_vdifheader_seconds_from_epoch(cached_header):
    assert cached_header.seconds_from_epoch == 7100400

@pytest.mark.parametrize("value, raw_value", [
    (86400, "10101000110000000"), 
    (8640060, "100000111101011000111100"),
    (1073741823, "111111111111111111111111111111")])
def test_vdifheader_seconds_from_epoch_assignment(cached_header, value, raw_value):
    cached_header.seconds_from_epoch = value
    _raw_value = switch_end(raw_value, Field.SECONDS_FROM_EPOCH._bit_length)
    assert cached_header.seconds_from_epoch == value
    assert cached_header._get_raw_value(Field.SECONDS_FROM_EPOCH) == _raw_value   

@pytest.mark.parametrize("value", [1073741824, "86400", "True"])
def test_vdifheader_seconds_from_epoch_assignment_invalid(cached_header, value):
    initial_value = cached_header.seconds_from_epoch
    inital_raw_value = cached_header._get_raw_value(Field.SECONDS_FROM_EPOCH)
    error = ValueError if type(value) == Field.SECONDS_FROM_EPOCH.data_type else TypeError
    with pytest.raises(error):
        cached_header.seconds_from_epoch = value
    assert cached_header.seconds_from_epoch== initial_value
    assert cached_header._get_raw_value(Field.SECONDS_FROM_EPOCH) == inital_raw_value  


# test unassigned_field field (get, set, attempt set invalid, warn on set incorrect)

def test_vdifheader_unassigned_field(cached_header):
    assert cached_header.unassigned_field == 0

@pytest.mark.parametrize("value, raw_value", [(0, "00")])
def test_vdifheader_unassigned_field_assignment(cached_header, value, raw_value):
    cached_header.unassigned_field = value
    _raw_value = switch_end(raw_value)
    assert cached_header.unassigned_field == value
    assert cached_header._get_raw_value(Field.UNASSIGNED_FIELD) == _raw_value

@pytest.mark.parametrize("value", [4, -1, 1.0, "1", True])
def test_vdifheader_unassigned_field_assignment_invalid(cached_header, value):
    initial_value = cached_header.unassigned_field
    inital_raw_value = cached_header._get_raw_value(Field.UNASSIGNED_FIELD)
    error = ValueError if type(value) == Field.UNASSIGNED_FIELD.data_type else TypeError
    with pytest.raises(error):
        cached_header.unassigned_field = value
    assert cached_header.unassigned_field == initial_value
    assert cached_header._get_raw_value(Field.UNASSIGNED_FIELD) == inital_raw_value  

@pytest.mark.skipif(os.environ.get("CAPSYS_WORKING") != "True",
    reason="capsys capture of stderr not working in current pytest")
@pytest.mark.parametrize("value, raw_value", [(1, "01"), (2, "10"), (3, "11")])
def test_vdifheader_unassigned_field_assignment_warning(cached_header, value, raw_value, capsys):
    cached_header.unassigned_field = value
    _stderr = capsys.readouterr().err
    _raw_value = switch_end(raw_value)
    assert cached_header.unassigned_field == value
    assert cached_header._get_raw_value(Field.UNASSIGNED_FIELD) == _raw_value
    assert f"ERROR: unassigned_field value should always be 0." in _stderr


# test reference_epoch field (get, set, attempt set invalid, warn on set incorrect)

def test_vdifheader_reference_epoch(cached_header):
    test_epoch = datetime(year=2021, month=7, day=1, tzinfo=timezone.utc)
    assert cached_header.reference_epoch == test_epoch

@pytest.mark.parametrize("value, raw_value", [
    (datetime(year=2020, month=7, day=1, tzinfo=timezone.utc), "101001"),
    (datetime(year=2000, month=1, day=1, tzinfo=timezone.utc), "000000")])
def test_vdifheader_reference_epoch_assignment(cached_header, value, raw_value):
    cached_header.reference_epoch = value
    _raw_value = switch_end(raw_value, Field.REFERENCE_EPOCH._bit_length)
    assert cached_header.reference_epoch == value
    assert cached_header._get_raw_value(Field.REFERENCE_EPOCH) == _raw_value

@pytest.mark.parametrize("value", [
    datetime(year=1999, month=1, day=1, tzinfo=timezone.utc),
    datetime(year=2000, month=2, day=1, tzinfo=timezone.utc),
    datetime(year=2000, month=1, day=30, tzinfo=timezone.utc),
    datetime(year=2032, month=1, day=1, tzinfo=timezone.utc),
    "2000-01-01", 20000101, True])
def test_vdifheader_reference_epoch_assignment_invalid(cached_header, value):
    initial_value = cached_header.reference_epoch
    inital_raw_value = cached_header._get_raw_value(Field.REFERENCE_EPOCH)
    error = ValueError if type(value) == Field.REFERENCE_EPOCH.data_type else TypeError
    with pytest.raises(error):
        cached_header.reference_epoch = value
    assert cached_header.reference_epoch == initial_value
    assert cached_header._get_raw_value(Field.REFERENCE_EPOCH) == inital_raw_value  

@pytest.mark.skipif(os.environ.get("CAPSYS_WORKING") != "True",
    reason="capsys capture of stderr not working in current pytest")
@pytest.mark.parametrize("value, raw_value", [
    (datetime(year=2030, month=1, day=1, tzinfo=timezone.utc), "111100")])
def test_vdifheader_reference_epoch_assignment_warning(cached_header, value, raw_value, capsys):
    cached_header.reference_epoch = value
    _stderr = capsys.readouterr().err
    _raw_value = switch_end(raw_value, Field.REFERENCE_EPOCH._bit_length)
    assert cached_header.reference_epoch == value
    assert cached_header._get_raw_value(Field.REFERENCE_EPOCH) == _raw_value
    assert f"WARNING: reference_epoch should not be in the future." in _stderr


# test data_frame_number field (get, set, attempt set invalid)

def test_vdifheader_data_frame_number(cached_header):
    assert cached_header.data_frame_number == 0

@pytest.mark.parametrize("value, raw_value", [
    (0, "0"),
    (500, "111110100"),
    (16777215, "111111111111111111111111")])
def test_vdifheader_data_frame_number_assignment(cached_header, value, raw_value):
    cached_header.data_frame_number = value
    _raw_value = switch_end(raw_value, Field.DATA_FRAME_NUMBER._bit_length)
    assert cached_header.data_frame_number == value
    assert cached_header._get_raw_value(Field.DATA_FRAME_NUMBER) == _raw_value

@pytest.mark.parametrize("value", [16777216, -1, 1.0, "1", True])
def test_vdifheader_data_frame_number_assignment_invalid(cached_header, value):
    initial_value = cached_header.data_frame_number
    inital_raw_value = cached_header._get_raw_value(Field.DATA_FRAME_NUMBER)
    error = ValueError if type(value) == Field.DATA_FRAME_NUMBER.data_type else TypeError
    with pytest.raises(error):
        cached_header.data_frame_number = value
    assert cached_header.data_frame_number == initial_value
    assert cached_header._get_raw_value(Field.DATA_FRAME_NUMBER) == inital_raw_value  


# test vdif_version field (get, set, attempt set invalid, warn on set incorrect)

def test_vdifheader_vdif_version(cached_header):
    assert cached_header.vdif_version == 0

@pytest.mark.parametrize("value, raw_value", [(1, "001"), (0, "000")])
def test_vdifheader_vdif_version_assignment(cached_header, value, raw_value):
    cached_header.vdif_version = value
    _raw_value = switch_end(raw_value)
    assert cached_header.vdif_version == value
    assert cached_header._get_raw_value(Field.VDIF_VERSION) == _raw_value

@pytest.mark.parametrize("value", [8, "1000", "1", True])
def test_vdifheader_vdif_version_assignment_invalid(cached_header, value):
    initial_value = cached_header.vdif_version
    inital_raw_value = cached_header._get_raw_value(Field.VDIF_VERSION)
    error = ValueError if type(value) == Field.VDIF_VERSION.data_type else TypeError
    with pytest.raises(error):
        cached_header.vdif_version = value
    assert cached_header.vdif_version== initial_value
    assert cached_header._get_raw_value(Field.VDIF_VERSION) == inital_raw_value  

@pytest.mark.skipif(os.environ.get("CAPSYS_WORKING") != "True",
    reason="capsys capture of stderr not working in current pytest")
@pytest.mark.parametrize("value, raw_value", [(2, "010"), (7, "111")])
def test_vdifheader_vdif_version_assignment_warning(cached_header, value, raw_value, capsys):
    cached_header.vdif_version = value
    _stderr = capsys.readouterr().err
    _raw_value = switch_end(raw_value)
    assert cached_header.vdif_version == value
    assert cached_header._get_raw_value(Field.VDIF_VERSION) == _raw_value
    assert f"WARNING: vdif_version {value} not recognised." in _stderr


# test num_channels field (get, set, attempt set invalid)

def test_vdifheader_num_channels(cached_header):
    assert cached_header.num_channels == 2

@pytest.mark.parametrize("value, raw_value",[
    (1, "0"),
    (65536, "10000"),
    (2147483648, "11111")])
def test_vdifheader_num_channels_assignment(cached_header, value, raw_value):
    cached_header.num_channels = value
    _raw_value = switch_end(raw_value, Field.NUM_CHANNELS._bit_length)
    assert cached_header.num_channels == value
    assert cached_header._get_raw_value(Field.NUM_CHANNELS) == _raw_value 

@pytest.mark.parametrize("value",[2147483649, 31, 0, -1, 1.0, "1", False])
def test_vdifheader_num_channels_assignment_invalid(cached_header, value):
    initial_value = cached_header.num_channels
    inital_raw_value = cached_header._get_raw_value(Field.NUM_CHANNELS)
    error = ValueError if type(value) == Field.NUM_CHANNELS.data_type else TypeError
    with pytest.raises(error):
        cached_header.num_channels = value
    assert cached_header.num_channels == initial_value
    assert cached_header._get_raw_value(Field.NUM_CHANNELS) == inital_raw_value  


# test data_frame_length field (get, set, attempt set invalid)

def test_vdifheader_data_frame_length(cached_header):
    assert cached_header.data_frame_length == 8032

@pytest.mark.parametrize("value, raw_value", [
    (40, "101"),
    (8032, "1111101100"),
    (6000, "1011101110"),
    (134217720, "111111111111111111111111")])
def test_vdifheader_data_frame_length_assignment(cached_header, value, raw_value):
    cached_header.data_frame_length = value
    _raw_value = switch_end(raw_value, Field.DATA_FRAME_LENGTH._bit_length)
    assert cached_header.data_frame_length == value
    assert cached_header._get_raw_value(Field.DATA_FRAME_LENGTH) == _raw_value  

@pytest.mark.parametrize("value", [134217721, 31, 0, -1, 1.0, "1", True])
def test_vdifheader_data_frame_length_assignment_invalid(cached_header, value):
    initial_value = cached_header.data_frame_length
    inital_raw_value = cached_header._get_raw_value(Field.DATA_FRAME_LENGTH)
    error = ValueError if type(value) == Field.DATA_FRAME_LENGTH.data_type else TypeError
    with pytest.raises(error):
        cached_header.data_frame_length = value
    assert cached_header.data_frame_length == initial_value
    assert cached_header._get_raw_value(Field.DATA_FRAME_LENGTH) == inital_raw_value 


# test data_type field (get, set, attempt set invalid)

def test_vdifheader_data_type(cached_header):
    assert cached_header.data_type == "real"

@pytest.mark.parametrize("value, raw_value", [("complex", "1"), ("real", "0")])
def test_vdifheader_data_type_assignment(cached_header, value, raw_value):
    cached_header.data_type = value
    assert cached_header.data_type == value
    assert cached_header._get_raw_value(Field.DATA_TYPE) == raw_value   

@pytest.mark.parametrize("value", ["COMPLEX", "imaginary", 1, True])
def test_vdifheader_data_type_assignment_invalid(cached_header, value):
    initial_value = cached_header.data_type
    inital_raw_value = cached_header._get_raw_value(Field.DATA_TYPE)
    error = ValueError if type(value) == Field.DATA_TYPE.data_type else TypeError
    with pytest.raises(error):
        cached_header.data_type = value
    assert cached_header.data_type == initial_value
    assert cached_header._get_raw_value(Field.DATA_TYPE) == inital_raw_value  


# test bits_per_sample field (get, set, attempt set invalid)

def test_vdifheader_bits_per_sample(cached_header):
    assert cached_header.bits_per_sample == 2

@pytest.mark.parametrize("value, raw_value",[
    (1, "0"),
    (32, "11111")])
def test_vdifheader_bits_per_sample_assignment(cached_header, value, raw_value):
    cached_header.bits_per_sample = value
    _raw_value = switch_end(raw_value, Field.BITS_PER_SAMPLE._bit_length)
    assert cached_header.bits_per_sample == value
    assert cached_header._get_raw_value(Field.BITS_PER_SAMPLE) == _raw_value  

@pytest.mark.parametrize("value",[0, 33, -1, 1.0, "1", True])
def test_vdifheader_bits_per_sample_assignment_invalid(cached_header, value):
    initial_value = cached_header.bits_per_sample
    inital_raw_value = cached_header._get_raw_value(Field.BITS_PER_SAMPLE)
    error = ValueError if type(value) == Field.BITS_PER_SAMPLE.data_type else TypeError
    with pytest.raises(error):
        cached_header.bits_per_sample = value
    assert cached_header.bits_per_sample == initial_value
    assert cached_header._get_raw_value(Field.BITS_PER_SAMPLE) == inital_raw_value  


# test thread_id field (get, set, attempt set invalid)

def test_vdifheader_thread_id(cached_header):
    assert cached_header.thread_id == 0

@pytest.mark.parametrize("value, raw_value",[
    (0, "0"),
    (1023, "1111111111")])
def test_vdifheader_thread_id_assignment(cached_header, value, raw_value):
    cached_header.thread_id = value
    _raw_value = switch_end(raw_value, Field.THREAD_ID._bit_length)
    assert cached_header.thread_id == value
    assert cached_header._get_raw_value(Field.THREAD_ID) == _raw_value  

@pytest.mark.parametrize("value", [1024, "256", -1, "aaa", True])
def test_vdifheader_thread_id_assignment_invalid(cached_header, value):
    initial_value = cached_header.thread_id
    inital_raw_value = cached_header._get_raw_value(Field.THREAD_ID)
    error = ValueError if type(value) == Field.THREAD_ID.data_type else TypeError
    with pytest.raises(error):
        cached_header.thread_id = value
    assert cached_header.thread_id == initial_value
    assert cached_header._get_raw_value(Field.THREAD_ID) == inital_raw_value  


# test station_id field (get, set, attempt set invalid)

def test_vdifheader_station_id(cached_header):
    assert cached_header.station_id == "Tt"

@pytest.mark.parametrize("value, raw_value", [
    ("Mp",  "01001101 01110000"), # 77 112 (ASCII) 
    ("125", "1111101"),
    ("16", "10000"),
    ("12287", "10111111111111")])
def test_vdifheader_station_id_assignment(cached_header, value, raw_value):
    cached_header.station_id = value
    if not value.isnumeric():
        raw_values = raw_value.split(" ")
        padded_values = ["".join(reversed(v.rjust(8, "0"))) for v in raw_values]
        _raw_value = "".join(padded_values)
    else:
        _raw_value = switch_end(raw_value, Field.STATION_ID._bit_length)
    assert cached_header.station_id == value
    assert cached_header._get_raw_value(Field.STATION_ID) == _raw_value

@pytest.mark.parametrize("value", ["12288", 256, -1, "aaa", True])
def test_vdifheader_station_id_assignment_invalid(cached_header, value):
    initial_value = cached_header.station_id
    inital_raw_value = cached_header._get_raw_value(Field.STATION_ID)
    error = ValueError if type(value) == Field.STATION_ID.data_type else TypeError
    with pytest.raises(error):
        cached_header.station_id = value
    assert cached_header.station_id == initial_value
    assert cached_header._get_raw_value(Field.STATION_ID) == inital_raw_value  


# test extended_data_version field (get, set, attempt set invalid, warn on set incorrect)

def test_vdifheader_extended_data_version(cached_header):
    assert cached_header.extended_data_version == 0

@pytest.mark.parametrize("value, raw_value",[
    (0x00, "00000000"),
    (0x01, "00000001"),
    (0x02, "00000010"),
    (0x03, "00000011"),
    (0x04, "00000100")])
def test_vdifheader_extended_data_version_assignment(cached_header, value, raw_value):
    cached_header.extended_data_version = value
    _raw_value = "".join(reversed(raw_value))
    assert cached_header.extended_data_version == value
    assert cached_header._get_raw_value(Field.EXTENDED_DATA_VERSION) == _raw_value  

@pytest.mark.parametrize("value", [256, -1, "1", True])
def test_vdifheader_extended_data_version_assignment_invalid(cached_header, value):
    initial_value = cached_header.extended_data_version
    inital_raw_value = cached_header._get_raw_value(Field.EXTENDED_DATA_VERSION)
    error = ValueError if type(value) == Field.EXTENDED_DATA_VERSION.data_type else TypeError
    with pytest.raises(error):
        cached_header.extended_data_version = value
    assert cached_header.extended_data_version == initial_value
    assert cached_header._get_raw_value(Field.EXTENDED_DATA_VERSION) == inital_raw_value  

@pytest.mark.skipif(os.environ.get("CAPSYS_WORKING") != "True",
    reason="capsys capture of stderr not working in current pytest")
@pytest.mark.parametrize("value, raw_value", [(0x05, "00000101")])
def test_vdifheader_extended_data_version_assignment_warning(cached_header, value, raw_value, capsys):
    cached_header.extended_data_version = value
    _stderr = capsys.readouterr().err
    _raw_value = switch_end(raw_value)
    assert cached_header.extended_data_version == value
    assert cached_header._get_raw_value(Field.EXTENDED_DATA_VERSION) == _raw_value
    assert f"WARNING: extended_data_version {value} not recognised." in _stderr


# test extended_data field (get, set, attempt set invalid, warn on set incorrect)

def test_vdifheader_extended_data(cached_header): 
    assert cached_header.extended_data == {}

# def test_vdifheader_extended_data_assignment(cached_header, value, raw_value):
# TODO

# def test_vdifheader_extended_data_assignment_invalid(cached_header, value):
# TODO

# def test_vdifheader_extended_data_assignment_warning(cached_header, value, rawvalue, capsys):
# TODO