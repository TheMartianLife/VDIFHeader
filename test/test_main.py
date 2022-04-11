import pytest
import vdifheader as vh

# TODO test input_files reconcilliation within os.path
# ... absolute path
# ... relative path
# ... home-relative path
# ... stringified path
# ... escaped path
# ... path with sh vars

# test handling of multiple values in input_files
# ... run on each
# ... warn/error on invalid, but retain prior valid results