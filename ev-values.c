#include "ev.h"
#include "util.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>


int main(int argc, char **argv) {

    // Parse arguments
    if ((argc != 4) || (strcmp(argv[1], "-k") != 0)) {
        fprintf(stderr, "Usage: ev-values -k 123 foo.ev\n");
        exit(1);
    }
    uint64_t event_code = atoll(argv[2]);
    char *path = argv[3];

    // Load the entire ev file.
    unsigned char *ev_data;
    uint64_t ev_size;
    read_path_or_die(path, &ev_data, &ev_size);

    // How much space will we need?
    uint64_t values_size;
    char *err;
    if ((err = kvtool_ev_values_size_for_event(ev_data, ev_size, event_code, &values_size))) {
        fatal_error(err);
    }

    // Extract the values
    unsigned char *values = malloc_or_die(values_size);
    if ((err = kvtool_ev_extract_values(ev_data, ev_size, event_code, values, values_size))) {
        fatal_error(err);
    }

    // Write the values
    if (values_size > 0) {
        fwrite_or_die(values, values_size, stdout);
    }

    return 0;
}
