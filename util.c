#include "util.h"


void fatal_error(char *message) {
    fprintf(stderr, "Error: %s\n", message);
    exit(1);
}


void* malloc_or_die(size_t size) {
    void *data = malloc(size);
    if (!data) {
        fatal_error("malloc failed");
    }
    return data;
}


void read_path_or_die(char *path, unsigned char **data_p, uint64_t *size_p) {
    FILE *file = fopen_or_die(path, "r");
    long size = ftell_file_size(file);
    unsigned char *data = malloc_or_die(size);
    fread_or_die(data, size, file);
    *data_p = data;
    *size_p = size;
}


long ftell_file_size(FILE *file) {
    fseek(file, 0, SEEK_END);
    long size = ftell(file);
    fseek(file, 0, SEEK_SET);
    return size;
}


FILE* fopen_or_die(char *path, char *mode) {
    FILE *file = fopen(path, mode);
    if (!file) {
        fatal_error("fopen");
    }
    return file;
}


void fread_or_die(void *dest, size_t size, FILE *file) {
    if (fread(dest, size, 1, file) != 1) {
        fatal_error("fread");
    }
}

void fwrite_or_die(void *src, size_t size, FILE *file) {
    if (fwrite(src, size, 1, file) != 1) {
        fatal_error("fwrite");
    }
}
