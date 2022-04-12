import os, pytest
from vdifheader._utils import *
pytestmark = pytest.mark.fast


# THIS TEST WON'T WORK UNLESS GIVEN YOUR MACHINE-SPECIFIC PATHS
@pytest.mark.parametrize("path, absolute_path", [
    ("~/VDIFHeader", "/Users/mars/VDIFHeader"),
    ("./../../../mars/VDIFHeader", "/Users/mars/VDIFHeader"),
    ("~/Desktop/../VDIFHeader", "/Users/mars/VDIFHeader")])
@pytest.mark.skip(reason="cannot work unless given machine-specific paths")
def test_utils_test_sanitized_path(path, absolute_path):
    assert sanitized_path(path) == absolute_path


@pytest.mark.parametrize("input, switched_input", [
    ("1", "1"), 
    ("00000001", "10000000"),
    ("000100011100001110", ("011100001110001000"))])
def test_utils_test_switch_end(input, switched_input):
    assert switch_end(input) == switched_input


@pytest.mark.skipif(os.environ.get("CAPSYS_WORKING") != "True",
    reason="capsys capture of stderr not working in current pytest")
def test_utils_test_vh_warn(capsys):
    vh_warn("this is a test warning")
    test_output = "WARNING: this is a test warning."
    _stderr = capsys.readouterr().err
    assert test_output in _stderr


@pytest.mark.skipif(os.environ.get("CAPSYS_WORKING") != "True",
    reason="capsys capture of stderr not working in current pytest")
def test_utils_test_vh_error(capsys):
    vh_error("this is a test error")
    test_output = "ERROR: this is a test error."
    _stderr = capsys.readouterr().err
    assert test_output in _stderr


@pytest.mark.parametrize("value",[1, 10000000000])
def test_utils_posint(value):
    assert posint(value) == value


@pytest.mark.parametrize("value",[0, -2, -10000000000])
def test_utils_posint_invalid(value):
    with pytest.raises(ValueError):
        posint(value)


@pytest.mark.parametrize("station_id, station_info", [
    ("Mp", "Moprah, Australia"), 
    ("mp", "Unknown Station"),
    ("__", ("Unknown Station"))])
def test_utils_station_information(station_id, station_info):
    assert station_information(station_id) == station_info
