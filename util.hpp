#include "leveldb/db.h"

char* dir_arg_or_die(int argc, char **argv);
leveldb::DB* open_db(char *path);

void* malloc_or_die(size_t size);
void fwrite_or_die(void *data, size_t size, FILE *file);
void fatal_error(std::string message);
