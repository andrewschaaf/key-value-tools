#include "util.hpp"


void process_items(FILE *file, leveldb::DB* db);


int main(int argc, char **argv) {
    char *dir = dir_arg_or_die(argc, argv);
    leveldb::DB *db = open_db(dir);
    process_items(stdin, db);
    return 0;
}


void process_items(FILE *file, leveldb::DB* db) {

    uint32_t kv_capacity = 15000000;
    uint32_t kv_size;
    uint8_t *kv_data = (uint8_t *)malloc_or_die(kv_capacity);
    void *k_data = kv_data;
    void *v_data;

    uint64_t num_items = 0;

    uint32_t sizes[2];
    uint32_t bytes_read;
    while ((bytes_read = fread(sizes, 1, 8, file)) == 8) {
        kv_size = sizes[0] + sizes[1];

        // increase capacity if needed
        if (kv_size > kv_capacity) {
            free(kv_data);
            kv_capacity = kv_size;
            kv_data = (uint8_t *)malloc_or_die(kv_capacity);
        }

        // read key, value
        if (kv_size > 0) {
            if (fread(kv_data, kv_size, 1, file) != 1) {
                fatal_error("unexpected EOF");
            }
        }
        v_data = kv_data + sizes[0];

        std::string key(
            reinterpret_cast<const char *>(k_data),
            reinterpret_cast<const char *>(k_data) + sizes[0]
        );

        std::string value(
            reinterpret_cast<const char *>(v_data),
            reinterpret_cast<const char *>(v_data) + sizes[1]
        );

        leveldb::Status s = db->Put(leveldb::WriteOptions(), key, value);
        if(!s.ok()) {
            fatal_error("writing an item");
        }

        num_items++;
    }
    if (bytes_read != 0) {
        fatal_error("unexpected EOF");
    }

    if (num_items > 0) {
        // flush db by Put-ing the most recent item again (sync)
        std::string key(
            reinterpret_cast<const char *>(k_data),
            reinterpret_cast<const char *>(k_data) + sizes[0]
        );
        std::string value(
            reinterpret_cast<const char *>(v_data),
            reinterpret_cast<const char *>(v_data) + sizes[1]
        );
        leveldb::WriteOptions write_options;
        write_options.sync = true;
        leveldb::Status s = db->Put(write_options, key, value);
        if(!s.ok()) {
            fatal_error("writing an item");
        }
    }
}
