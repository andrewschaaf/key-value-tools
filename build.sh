mkdir -p build

export LEVELDB_DIR="/usr/local/Cellar/leveldb/1.15.0_1"
export LEVELDB_LIB="$LEVELDB_DIR/lib/libleveldb.1.15.dylib"
export LEVELDB_FLAGS="-I $LEVELDB_DIR/include $LEVELDB_LIB"
export ARGS="-std=c++11 -Wall -O3 $LEVELDB_FLAGS util.cpp"

echo "Compiling ./build/kv32-to-leveldb..." &&
  g++ $ARGS -o build/kv32-to-leveldb kv32-to-leveldb.cpp &&
  echo "Compiling ./build/leveldb-to-kv32..." &&
  g++ $ARGS -o build/leveldb-to-kv32 leveldb-to-kv32.cpp &&
  echo "Done."
