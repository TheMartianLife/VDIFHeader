import os, pytest
from vdifheader import VDIFHeader
from vdifheader._utils import sanitized_path

os.environ.setdefault("CAPSYS_WORKING", "False")
# TODO set to "True" after pytest issue #5997 is addressed
# to re-enable tests that verify generation of warnings
# https://github.com/pytest-dev/pytest/issues/5997

@pytest.fixture(scope="session", autouse=True)
def test_filepath():
    return sanitized_path("./test.vdif")

@pytest.fixture(scope="session", autouse=True)
def cached_header(test_filepath):
    header = None
    with open(test_filepath, "rb") as input_file:
        raw_header = input_file.read(32)
        header = VDIFHeader.parse(raw_header)
    assert header is not None
    return header
