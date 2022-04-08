# How to Use VDIF Header

## Installation

TODO

## Usage

TODO

## Types, Values and Functions

**Top-level public API functions**

```python
get_first_header(input_filepath: str) -> Optional[VDIFHeader]
```

Attempts to fetch first 32 bytes from file at `input_filepath`, interpret them as a VDIF header, and return a `VDIFHeader` object populated with `VDIFHeaderField` objects for each value found within the raw data. If file cannot be read, return value is `None`.

```python
get_headers(input_filepath: str, count: Optional[int]=None) -> list[VDIFHeader]:
```
Attempts to fetch sufficient bytes from file at `input_filepath` to populate `count` `VDIFHeader` objects, each populated with `VDIFHeaderField` objects. If file cannot be read, return value is an empty list. If `count` is negative or `None`, the function will attempt to parse all headers present in the file.

> :warning: **WARNING**: This function uses inbuilt `data_frame_length` values (specified in each header) to find subsequent headers. For example, if `header 0` says its frame is `8032 bytes` long, the function will interpet the data at `(location_of_this_header + 8032)` as the next header. This allows for warning of headers which defy the VDIF spec (which says all data frames in a file should be of equal length), but may result in error if this field of a single header is mangled.


### Output Modes

| Option | Description |
|:---|:---|
| `none` | No output (only show process errors) |
| `raw` | Output original binary data |
| `values` | Output `key: value` for each header field |
| `summary` | Output validation warnings and errors |
| `verbose` | Combined `raw`, `values`, and `summary` |

**Example output: `raw` mode**

```
       |     Byte 3    |     Byte 2    |     Byte 1    |     Byte 0    |
Word 0 |0|0|0 0 0 0 1 1 1 1 1 1 1 0 1 0 1 0 0 0 1 1 0 1 1 0 0 0 0 0 0 0|
Word 1 |0 0|1 1 0 1 0 1|0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0|
Word 2 |0 0 0|1 0 0 0 0|0 0 1 1 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0|
Word 3 |0|1 0 0 0 0|0 0 0 0 0 0 0 0 0 0|0 0 1 0 1 1 1 0 0 0 1 0 1 0 1 0|
Word 4 |0 0 0 0 0 0 0 0|0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0|
Word 5 |0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0|
Word 6 |0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0|
Word 7 |0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0|
```

**Example output: `values` mode**

```
Invalid flag: False
Legacy mode: False
Time from epoch: 7100400 seconds
Reference epoch: 2021-07-01 UTC
Data frame number: 0
VDIF version: 0
Number of channels: 2
Data frame length: 8032 bytes
Data type: real
Bits per sample: 2 bit(s)
Thread ID: 0
Station ID: Tt
Extended data version: 0
```

**Example output: `summary` mode**

```
WARNING: station id not in known list (header 0).
0 errors, 1 warnings generated.
```
