#include <stdlib.h>
#include <stdio.h>

void fatal_error(char *message);
void* malloc_or_die(size_t size);
void read_path_or_die(char *path, unsigned char **data_p, uint64_t *size_p);
long ftell_file_size(FILE *file);
FILE* fopen_or_die(char *path, char *mode);
void fread_or_die(void *dest, size_t size, FILE *file);
void fwrite_or_die(void *src, size_t size, FILE *file);
