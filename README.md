<img align="right" src="docs/logo.png" style="padding:10px;width:20%;">

# VDIF Header

[![Python 3.6](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/) [![GPL3+](https://img.shields.io/badge/license-GPL3+-blue)](https://www.gnu.org/licenses/gpl-3.0.en.html)

> :warning: **WARNING**: this software is in a pre-release state. Installation can only be done by downloading and running as a local module, and test coverage is not guaranteed.

A simple Python library for parsing and validating the format and values of **VDIF**[^1] headers in radio telescope data files.

When you work in the domain of VLBI astronomy or space domain awareness, you are forever relying on data files which are difficult to examine. So whenever you work on software that interprets it, you have to wonder every time it crashes whether it is the software or you. 

With this library, it's quick to inspect header values and you'll see printed warnings whenever something's awry. It's great for when you want to quickly check why [mark5access](https://safe.nrao.edu/wiki/bin/view/VLBA/Software#DiFX) is yelling at you, but if you need the actual frame content—or want to do more complex stuff with VDIF data in Python—you probably want to use [baseband](https://github.com/mhvk/baseband) instead.

[^1]: VLBI Data Interchange Format (source: [vlbi.org](https://vlbi.org/wp-content/uploads/2019/03/VDIF_specification_Release_1.1.1.pdf))

## Usage

This shows minimal working examples for different usage modes. For more detailed usage information, see the [vdifheader documentation](/docs).

### As a Package

When imported as a package, users have access to two main methods:

* `get_first_header(input_filepath)` - method returns the first header in the provided file as a `VDIFHeader` object.
* `get_headers(input_filepath, count=None)` - iterator method returns the first `count` headers in the provided file, as a **iterator**[^2] of `VDIFHeader` objects. If `count` is negative, zero or `None`, default behaviour is to parse all headers found in the file. 

> :brain: **REMEMBER**: Python iterators are very fast for large input, but are consumed if operated on. So if you write `output = some_iterator()` and then iterate over `output` (e.g. `for item in output`), the output will now be empty.

[^2]: Iterators in Python are a type of method that *generates* a result, rather than *returns* a result. For operating over potentially large input, this means not waiting for the whole thing to be loaded into memory before starting work (see: [wiki.python.org](https://wiki.python.org/moin/Iterator)).

```python
import vdifheader as vh
from vdifheader import Validity

input_filepath = './some_input_file.vdif'

# get some headers
headers = vh.get_headers(input_filepath, count=5) # as iterator (fast)
headers_list = list(headers) # as list (sticks around)
for header in headers_list:
    header.print_summary()

# do stuff with a header
first_header = headers_list[0]
timestamp = first_header.get_timestamp()
print(f"\n\nParsed {len(headers_list)} starting at: {timestamp}")
print(f"Source station: {first_header.get_station_information()}")

# export its values somewhere
first_header.to_csv(output_filepath='./some_input_file_vdif.csv')
```
Output:
```
ERROR: reference epoch is in the future (header 4).

Parsed 5 starting at: 2021-09-21 04:20:00+00:00
Source station: Moprah, Australia
```

### As a Script

When run as a script, simply specify a file to validate and any additional configuration options. Options include:

* show usage/help
* parse only a certain number of headers
* show output in a certain format

```
% python -m vdifheader -h
usage: vdifheader [options] [file]
  options:
    -h, --help		    show help
    -n --count [number]	number of headers to parse (default=1)
    -a --all		    parse all headers in file
    -v --values         show values output
    -b --binary		    show raw binary output
%
% python -m vdifheader some_input_file.vdif
ERROR: unassigned_field value should always be 0.
WARNING: vdif_version value > 1 not recognised.
```

### As an Interactive Script

When passing `-i` to the Python interpreter, the provided script will run but leave the interpreter open afterwards for the user to continue the session with variable memory and declarations intact. In this mode, after completion of the script, the following values will be set:

* `first_header` - the first header parsed from the provided file.
* `headers` - a list of all headers parsed from the provided file.

```
% python -i -m vdifheader --count 5 some_input_file.vdif
ERROR: unassigned_field value should always be 0.
WARNING: vdif_version value > 1 not recognised.
>>> first_header.station_id
Mp
>>> len(headers)
5
```

For detailed usage information, see the [vdifheader documentation](/docs).

## License

This project is licensed under the terms of the [GNU General Public License, version 3](https://www.gnu.org/licenses/gpl-3.0.en.html). **This is a [copyleft](https://www.gnu.org/licenses/copyleft.en.html) license.**

## Planned Improvements

- [ ] Handling of Extended Data fields.
- [ ] Write values back to valid binary header of type `bytes`.
- [x] Output header values to formats such as ~~iniFile~~/~~csv~~/json/~~dict~~.
