#include "util.hpp"


void process_items(leveldb::DB* db, FILE *file);


int main(int argc, char **argv) {
    char *dir = dir_arg_or_die(argc, argv);
    leveldb::DB *db = open_db(dir);
    process_items(db, stdout);
    return 0;
}


void process_items(leveldb::DB* db, FILE *file) {
    uint32_t sizes[2];
    leveldb::Iterator* it = db->NewIterator(leveldb::ReadOptions());
    for (it->SeekToFirst(); it->Valid(); it->Next()) {

        // key
        std::string key = it->key().ToString();
        sizes[0] = key.size();
        void *key_data = (void *)key.data();

        // value
        std::string value = it->value().ToString();
        sizes[1] = value.size();
        void *value_data = (void *)value.data();

        // write item
        fwrite_or_die(sizes, 8, file);
        if (sizes[0] > 0) {
            fwrite_or_die(key_data, sizes[0], file);
        }
        if (sizes[1] > 0) {
            fwrite_or_die(value_data, sizes[1], file);
        }
    }
}
