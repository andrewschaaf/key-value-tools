#include <stdint.h>

char* kvtool_ev_values_size_for_event(void *ev, uint64_t ev_size, uint64_t event_code, uint64_t *values_size);
char* kvtool_ev_extract_values       (void *ev, uint64_t ev_size, uint64_t event_code, void *values, uint64_t values_size);
