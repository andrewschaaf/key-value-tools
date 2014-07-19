**Tools for (bytes, bytes)-list streams/files/databases**

### Tools

    ... | kv32-to-leveldb $DB_DIR
    leveldb-to-kv32 $DB_DIR | ...


### Building

    brew install leveldb
    bash build.sh


### kv32 format

The kv32 bytestream is a concatenation of zero or more of these:

    key_size    : uint32le
    value_size  : uint32le
    key         : bytes
    value       : bytes


### TODO

Support these:

- Hadoop SequenceFile
- Cassandra bulk import/export JSON


### [License: MIT](LICENSE.txt)
