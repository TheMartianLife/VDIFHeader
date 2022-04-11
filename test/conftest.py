import pytest
from os import path

@pytest.fixture(scope="session", autouse=True)
def test_file():
    return path.abspath("./test.vdif")
