mkdir -p build

export LEVELDB_DIR="/usr/local/Cellar/leveldb/1.15.0_1"
export LEVELDB_LIB="$LEVELDB_DIR/lib/libleveldb.1.15.dylib"
export LEVELDB_FLAGS="-I $LEVELDB_DIR/include $LEVELDB_LIB"
export CPP_ARGS="-std=c++11 -Wall -O2 $LEVELDB_FLAGS util.cpp"
export C_ARGS="-std=c99 -Wall -O2 util.c ev.c"

echo "Compiling ./build/kv32-to-leveldb..." &&
  g++ $CPP_ARGS -o build/kv32-to-leveldb kv32-to-leveldb.cpp &&
  echo "Compiling ./build/leveldb-to-kv32..." &&
  g++ $CPP_ARGS -o build/leveldb-to-kv32 leveldb-to-kv32.cpp &&
  echo "Compiling ./build/libkvtools.so..." &&
  gcc -c -Wall -O2 -Wall -std=c99 -fPIC -o ./build/ev.o ev.c &&
  gcc -o ./build/libkvtools.so -shared ./build/ev.o &&
  echo "Compiling ./build/ev-values..." &&
  gcc $C_ARGS -o build/ev-values ev-values.c &&
  echo "Done."
