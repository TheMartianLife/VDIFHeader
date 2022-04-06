<img align="right" src="docs/logo.png" style="padding:10px;width:30%;max-width:220px;min-width:100px;">

# VDIF Header
A simple Python library for parsing and validating the format and values of **VDIF**[^1] headers in radio telescope data files.

[^1]: VLBI Data Interchange Format (source: [vlbi.org](https://vlbi.org/wp-content/uploads/2019/03/VDIF_specification_Release_1.1.1.pdf))

## Usage

### As a Package

When imported as a package, users have access to two main functions:

* `get_first_header(input_filepath)` - function returns the first header in the provided file as a `VDIFHeader` object.
* `get_headers(input_filepath, count=None)` - generator function returns the first `count` headers in the provided file, either as a generator (e.g. `for h in get_headers(input_filepath)` or as a list of `VDIFHeader` objects. If `count` is negative, zero or `None`, default behaviour is to parse is all headers in file.

```python
import vdifheader

intput_filepath = './some_input_file.vdif'
headers = get_headers(input_filepath, count=5)
timestamp = headers[0].get_timestamp()
print(f"Parsed {len(headers)} starting at {timestamp}")
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
    -h, --help		show help
    -n --count [number]	number of headers to parse (default=all)
    -a --all		parse all headers in file
    -v --verbose	show all output
    -s --silent		show minimal output
    -p --print [mode]	level of output to show {none|summary|values|raw|verbose}
%
% python -m vdifheader some_input_file.vdif
WARNING: synch code field contains incorrect value (header 2).
WARNING: synch code field contains incorrect value (header 3).
0 errors, 2 warnings generated.
```

### As an Interactive Script

When passing `-i` to the Python interpreter, the provided script will run but leave the interpreter open afterwards for the user to continue the session with variable memory and declarations intact. In this mode, after completion of the script, the following values will be set:

* `first_header` - the first header parsed from the provided file.
* `headers` - an array of all headers parsed from the provided file.

```
% python -m vdifheader --count 5 some_input_file.vdif
WARNING: synch code field contains incorrect value (header 2).
WARNING: synch code field contains incorrect value (header 3).
0 errors, 2 warnings generated.
>>> first_header.station_id
Hb
>>> len(headers)
5
```

For detailed usage information, see the [vdifheader documentation](/docs).

## License

This project is licensed under the terms of the [GNU General Public License, version 3](https://www.gnu.org/licenses/gpl-3.0.en.html). **This is a [copyleft](https://www.gnu.org/licenses/copyleft.en.html) license.**
