# How to Use VDIF Header

**Contents**

* [Installation instructions](#installation)
* [API functions](#api_functions)
* [The `VDIFHeader` class](#vdifheader)
* [The `VDIFHeaderField` class](#vdifheaderfield)
* [Output modes](#output_modes)

<a name="installation"></a>
## Installation

TODO

<a name="api_functions"></a>
## **Top-level public API functions**

```python
get_first_header(input_filepath: str) -> Optional[VDIFHeader]
```

Attempts to fetch first 32 bytes from file at `input_filepath`, interpret them as a VDIF header, and return a `VDIFHeader` object populated with `VDIFHeaderField` objects for each value found within the raw data. If file cannot be read, return value is `None`.

```python
get_headers(input_filepath: str, count: Optional[int]=None) -> Iterator[VDIFHeader]
```

Attempts to fetch sufficient bytes from file at `input_filepath` to populate `count` `VDIFHeader` objects, each populated with `VDIFHeaderField` objects. If file cannot be read, return value is an empty list. If `count` is negative or `None`, the function will attempt to parse all headers present in the file.

> :warning: **WARNING**: This function uses inbuilt `data_frame_length` values (specified in each header) to find subsequent headers. For example, if `header 0` says its frame is `8032 bytes` long, the function will interpet the data at `(location_of_this_header + 8032)` as the next header. This allows for warning of headers which defy the VDIF spec (which says all data frames in a file should be of equal length), but may result in error if this field of a single header is mangled.

<a name="vdifheader"></a>
## **Module classes: `VDIFHeader`**

**Attributes**

```python
invalid_flag: VDIFHeaderField
legacy_mode: VDIFHeaderField
seconds_from_epoch: VDIFHeaderField
unassigned_field: VDIFHeaderField
reference_epoch: VDIFHeaderField
data_frame_number: VDIFHeaderField
vdif_version: VDIFHeaderField
num_channels: VDIFHeaderField
data_frame_length: VDIFHeaderField
data_type: VDIFHeaderField
bits_per_sample: VDIFHeaderField
thread_id: VDIFHeaderField
station_id: VDIFHeaderField
extended_data_version: VDIFHeaderField
extended_data: VDIFHeaderField
```

Attributes that represent header **fields**.

```python
warnings: list[str]
warnings_count: int
errors: list[str]
errors_count: int
```

Utility attributes used for displaying aggregated information about completed validity checks.

```python
raw_data: Optional[list[str]]
```

The raw input used to construct the object, represented as a list of `8` strings where each string is a data word where the [endianness](https://en.wikipedia.org/wiki/Endianness) has been switched from little-endian (which makes sense for computers) to big-endian (which makes sense for humans accessing indices). This means that where the raw bits on disk may be `ddddddddccccccccbbbbbbbbaaaaaaaa`, the word string will be in order `aaaaaaaabbbbbbbbccccccccdddddddd`. This means that accessing e.g., word `1`, bit `23` is as easy as `raw_data[1][23]`.

```python
header_num: Optional[int]
```

Used to validate a header's `data_frame_number` based on their position in a file and the values of other headers in the same file. In debug output, `"(header {n})"` uses this number as `n`.

**Functionss**

```python
@staticmethod parse(raw_data: bytes, header_num: Optional[int]=None) -> VDIFHeader
```

Creates a new `VDIFHeader` object populated from values present in the `raw_data` bytes, as per the [VDIF format specification](https://vlbi.org/wp-content/uploads/2019/03/VDIF_specification_Release_1.1.1.pdf).

```python
get_timestamp() -> datetime
```

Combines the header's `reference_epoch` and `seconds_from_epoch` values into a single `datetime` object.

```python
print_summary()
print_raw()
print_values()
print_verbose()
```

Prints the content of the header as per [output formats](/output_formats).

```python
to_dict() -> dict[str, Union[bool, int, str]]
get_extended_data_dict() -> dict[str, Union[bool, int, str]]
```

Creates `dict` of header fields as format `field_name: field_value`. The result of `to_dict()` **includes** values from `get_extended_data_dict()`, but the latter can be used in other operations to get just the fields that are not always included in a VDIF header.

```python
to_inifile(output_filepath: str)
to_csv(output_filepath: str)
```

Sends header field names and field values to the output file in the requested format. Here, `inifile` format is `{field_name}={field_value}\n` and `csv` includes column names `field_name` and `field_value`. Fields from extended data are only included if the extended data version is valid, the extended data format is known, and the value is set.

<a name="vdifheaderfield"></a>
## **Module classes: `VDIFHeaderField`**

**Attributes**

```python
value: Union[bool, int, str]
```

The human-interpretable value of the field. In the case of `reference_epoch`, the string represents an [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) date value. 

> :warning: **WARNING**: In the case of `extended_data` this string is an aggregate value and should not be used; instead, the parent `VDIFHeader`'s `get_extended_data_dict()` should be used to fetch specific values, after checking for their presence.

```python
raw_value: str
```

A string representing the bits from the parent `VDIFHeader`'s `raw_data` that correspond to (and were used to form) this value. 

> :warning: **WARNING**: This is not guaranteed to match (or be convertible to) `value`, as some fields undergo transformation after read. For example, the `num_channels` field, where the resulting `value` is `2 ** (raw_value)`; or `station_id`, where the field may or may not be converted to [ASCII](https://en.wikipedia.org/wiki/ASCII) depending on the `raw_value`.

```python
validity: Validity
```

An `enum` value of type `Validity`, where possible values are `VALID`, `INVALID`, or `UNKNOWN`.

<a name="output_modes"></a>
## Output Modes

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
