#pragma once
#include <filesystem>
#include <iostream>
#include <fstream>
#include <stdint.h>
#include "./rules.cpp"
inline void morkReadMetadata(morkrepository* repository, std::fstream& stream) {
  stream.read(reinterpret_cast<char*>(repository), sizeof(morkrepository));
}
inline void morkReadMetadata(morkchunker* chunker, std::fstream& stream) {
  stream.read(reinterpret_cast<char*>(chunker), sizeof(morkchunker));
}
inline void morkUpdateRepositoryMetadata(morkrepository* repository, std::fstream& stream) {
  stream.seekp(0);
  morkValidateSignature(stream);
  stream.write(reinterpret_cast<const char*>(repository), sizeof(morkrepository));
}
bool morkGetChunkerMetadata(const uint8_t* repositories, const size_t length, const uint8_t chunkerIndex, morkchunker* chunker);
bool morkGetChunkerBySize(const std::streamsize size, std::filesystem::path* entry, morkchunker* chunker, uint8_t* index);