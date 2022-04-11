import pytest

from vdifheader._utils import *

# THIS TEST WON'T WORK UNLESS GIVEN YOUR MACHINE-SPECIFIC PATHS
# @pytest.mark.fast
# @pytest.mark.parametrize("path, absolute_path", [
#     ("~/VDIFHeader", "/Users/mars/VDIFHeader"),
#     ("./../../../mars/VDIFHeader", "/Users/mars/VDIFHeader"),
#     ("~/Desktop/../VDIFHeader", "/Users/mars/VDIFHeader")])
# def test_utils_test_sanitized_path(path, absolute_path):
#     assert sanitized_path(path) == absolute_path

@pytest.mark.fast
@pytest.mark.parametrize("input, switched_input", [
    ("1", "1"), 
    ("00000001", "10000000"),
    ("000100011100001110", ("011100001110001000"))
])
def test_utils_test_switch_end(input, switched_input):
    assert switch_end(input) == switched_input


def test_utils_test_vh_warn():
    test_message = "this is a test warning"
    test_output = "\033[0;33mWARNING: this is a test warning.\033[0m\n"
    # TODO re-include after pytest issue #5997 is addressed
    # https://github.com/pytest-dev/pytest/issues/5997
    # _stderr = capsys.readouterr().err
    # assert _stdout == test_output

def test_utils_test_vh_error():
    test_message = "this is a test error"
    test_output = "\033[0;31mERROR: this is a test error.\033[0m\n"
    # TODO re-include after pytest issue #5997 is addressed
    # https://github.com/pytest-dev/pytest/issues/5997
    # _stderr = capsys.readouterr().err
    # assert _stdout == test_output


@pytest.mark.fast
@pytest.mark.parametrize("station_id, station_info", [
    ("Mp", "Moprah, Australia"), 
    ("mp", "Unknown Station"),
    ("__", ("Unknown Station"))
])
def test_utils_station_information(station_id, station_info):
    assert station_information(station_id) == station_info
