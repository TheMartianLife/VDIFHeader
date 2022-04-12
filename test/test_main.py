import os, pytest, sys
from vdifheader._utils import sanitized_path
from vdifheader.__main__ import *
pytestmark = pytest.mark.fast

# TODO test input_files reconcilliation within os.path
# ... stringified path
# ... escaped path
# ... path with sh vars


# test handling of command line args

@pytest.mark.parametrize("headers_arg, num_headers", [
    ("-n 10", 10),
    ("--count 1000000", 1000000),
    ("-a", -1),
    ("--all", -1),
    ("", 1)])
@pytest.mark.parametrize("output_arg, output_mode", [
    ("-v", VDIFOutputMode.VALUES), 
    ("--values", VDIFOutputMode.VALUES), 
    ("-b", VDIFOutputMode.BINARY), 
    ("--binary", VDIFOutputMode.BINARY),
    ("", VDIFOutputMode.VALUES)])
@pytest.mark.parametrize("input_arg, input_file", [
    ("./test.vdif", sanitized_path("./test.vdif"))])
def test_main_arg_parser(headers_arg, num_headers, output_arg, output_mode, input_arg, input_file):
    args = f"{headers_arg} {output_arg} {input_arg}".split(" ")
    args = [arg for arg in args if arg != ""]
    parsed_args = vars(arg_parser().parse_args(args))
    assert parsed_args["num_headers"] == num_headers
    assert parsed_args["output_mode"] == output_mode
    assert parsed_args["input_file"] == input_file


# test run of main() method

def test_main_method(test_filepath):
    sys.argv = ["vdifheader.py", test_filepath]
    main()