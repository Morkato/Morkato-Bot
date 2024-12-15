#pragma once
#include "./settings.cpp"
#include "./rules.cpp"
#include <filesystem>
#include <string.h>
#include <iostream>
#include <fstream>
#include <vector>

const char* MORKATO_STORAGE_LOCATION;
const char* MORKATO_TMP_LOCATION;
std::vector<morkchunk> MORKATO_ZEROS_CHUNKS;
std::vector<morkchunker> MORKATO_ZEROS_CHUNKERS;
std::vector<char> MORKATO_ZEROS;
std::size_t MORKATO_BUFFER_LENGTH;
bool MORKATO_STORAGE = false;
void morkStorageInit(const morksettings& settings) {
  namespace fs = std::filesystem;
  MORKATO_STORAGE_LOCATION = settings.morkstorage_location;
  MORKATO_TMP_LOCATION = settings.morktmp_location;
  if (!fs::exists(MORKATO_STORAGE_LOCATION)) {
    fs::create_directory(MORKATO_STORAGE_LOCATION);
  }
  if (!fs::exists(MORKATO_TMP_LOCATION)) {
    fs::create_directory(MORKATO_TMP_LOCATION);
  }
  MORKATO_ZEROS = std::vector<char>(settings.morkbuf_length, '\0');
  MORKATO_ZEROS_CHUNKS = std::vector<morkchunk>(MORKATO_LENGTH_MAX, morkchunk {0, 0});
  MORKATO_ZEROS_CHUNKERS = std::vector<morkchunker>(MORKATO_LENGTH_MAX, morkchunker {0, 0});
  MORKATO_BUFFER_LENGTH = settings.morkbuf_length;
  MORKATO_STORAGE = true;
}
void morkStorageClose() {
  MORKATO_ZEROS.clear();
  MORKATO_ZEROS.shrink_to_fit();
  MORKATO_ZEROS_CHUNKS.clear();
  MORKATO_ZEROS_CHUNKS.shrink_to_fit();
  MORKATO_ZEROS_CHUNKERS.clear();
  MORKATO_ZEROS_CHUNKERS.shrink_to_fit();
}