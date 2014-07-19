#include "util.hpp"
#include <assert.h>


char *dir_arg_or_die(int argc, char **argv) {
    if (argc != 2) {
        fatal_error("expected exactly one argument: the LevelDB dir");
    }
    return argv[1];
}


leveldb::DB* open_db(char *dbDir) {
    leveldb::DB* db;
    leveldb::Options options;
    options.create_if_missing = true;
    leveldb::Status status = leveldb::DB::Open(options, dbDir, &db);
    if (!status.ok()) {
        fatal_error("opening the LevelDB database");
    }
    return db;
}


void* malloc_or_die(size_t size) {
    void *data = malloc(size);
    if (!data) {
        fatal_error("malloc failed");
    }
    return data;
}


void fwrite_or_die(void *data, size_t size, FILE *file) {
    if (fwrite(data, size, 1, file) != 1) {
        fatal_error("fwrite");
    }
}


void fatal_error(std::string message) {
    fprintf(stderr, "Error: %s\n", message.c_str());
    exit(1);
}
