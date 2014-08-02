**Tools for (key, value)-list streams/files/databases**

[![Build Status](https://secure.travis-ci.org/andrewschaaf/key-value-tools.png)](http://travis-ci.org/andrewschaaf/key-value-tools)


### Command-line Tools

    ...kv32... | kv-map 'convert ppm:- png:-' | ...kv32...

    ... | kv32-to-leveldb $DB_DIR
    leveldb-to-kv32 $DB_DIR | ...

    ev-values -k $KEY foo.ev | ...concatenated values for key $KEY...


### Python Library (uses the C library under the hood)

To concatenate fixed-width events as a matrix:

```python
from kvtools import EVFile
m = EVFile(data).event_as_matrix(event_code, ncols=7, dtype=numpy.dtype('float64'))
```

Install it however you like, e.g. via:

    export PYTHONPATH="$PYTHONPATH:/.../key-value-tools/python"


### C Library

All functions return `NULL` or an error message.

```c
char* kvtool_ev_values_size_for_event(void *ev, uint64_t ev_size, uint64_t event_code, uint64_t *values_size);
char* kvtool_ev_extract_values       (void *ev, uint64_t ev_size, uint64_t event_code, void *values, uint64_t values_size);
```


### Building

    brew install leveldb
    bash build.sh


## Formats

### leveldb: (bytes, bytes)-list with unique keys

A [LevelDB](https://code.google.com/p/leveldb/) database directory.


### kv32: (bytes, bytes)-list

The kv32 bytestream is a concatenation of zero or more of these:

    key_size    : uint32le
    value_size  : uint32le
    key         : bytes
    value       : bytes


### ev: (uint64, bytes)-list

The ev bytestream is a concatenation of zero or more of these:

    event_code  : unsigned varint (protobuf-style)
    value_size  : unsigned varint (protobuf-style)
    value       : bytes


### TODO

Support these:

- SQLite file
- Hadoop SequenceFile
- Cassandra bulk import/export JSON
- SQL `INSERT` statements with N rows per statement


### [License: MIT](LICENSE.txt)
