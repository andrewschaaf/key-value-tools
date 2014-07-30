#include "ev.h"
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>


char* kvtool_ev_values_size_for_event(void *ev, uint64_t ev_size, uint64_t event_code_of_interest, uint64_t *values_size) {
    long result = 0;
    uint32_t event_code, value_size;
    uint8_t *p = ev;
    uint8_t *p_bound = p + ev_size;
    while (p < p_bound) {
        event_code = p[0];
        if (event_code > 127) {
            return "TODO: support varints > 127";
        }
        p++;
        if (p >= p_bound) {
            return "unexpected EOF after event code";
        }
        value_size = p[0];
        if (value_size > 127) {
            return "TODO: support varints > 127";
        }
        p++;
        p += value_size;
        if (p > p_bound) {
            return "unexpected EOF after value size";
        }
        if (event_code == event_code_of_interest) {
            result += value_size;
        }
    }
    *values_size = result;
    return NULL;
}


char* kvtool_ev_extract_values(void *ev, uint64_t ev_size, uint64_t event_code_of_interest, void *values, uint64_t values_size) {

    uint32_t event_code, value_size;
    uint8_t *p = ev;
    uint8_t *p_bound = p + ev_size;
    uint32_t values_pos = 0;

    while (p < p_bound) {
        event_code = p[0];
        if (event_code > 127) {
            return "TODO: support varints > 127";
        }
        p++;
        if (p >= p_bound) {
            return "unexpected EOF after event code";
        }
        value_size = p[0];
        if (value_size > 127) {
            return "TODO: support varints > 127";
        }
        p++;
        if ((p + value_size) > p_bound) {
            return "unexpected EOF after value size";
        }
        if (event_code == event_code_of_interest) {
            memcpy(&(values[values_pos]), p, value_size);
            values_pos += value_size;
        }
        p += value_size;
    }

    return NULL;
}
