#pragma once
#include <string.h>
#include <fstream>
#include <vector>
#include "./rules.hpp"
extern std::vector<morkchunk> MORKATO_ZEROS_CHUNKS;
extern std::vector<morkchunker> MORKATO_ZEROS_CHUNKERS;
void morkCreateChunkFile(std::fstream& stream) {
  char empty = '\0';
  stream.write(MORKATO_SIGNATURE, sizeof(char) * strlen(MORKATO_SIGNATURE));
  stream.write(reinterpret_cast<const char*>(&empty), sizeof(char));
  stream.write(reinterpret_cast<const char*>(MORKATO_ZEROS_CHUNKS.data()), sizeof(morkchunk) * MORKATO_LENGTH_MAX);
  stream.write(reinterpret_cast<const char*>(&empty), sizeof(char));
  stream.flush();
}
void morkCreateRepositoryFile(std::fstream& stream) {
  const morkrepository metadata {0,0};
  char empty = '\0';
  stream.write(MORKATO_SIGNATURE, sizeof(char) * strlen(MORKATO_SIGNATURE));
  stream.write(reinterpret_cast<const char*>(&empty), sizeof(char));
  stream.write(reinterpret_cast<const char*>(&metadata), sizeof(morkrepository));
  stream.write(reinterpret_cast<const char*>(MORKATO_ZEROS_CHUNKERS.data()), sizeof(morkchunker) * MORKATO_LENGTH_MAX);
  stream.flush();
}
bool morkValidateSignature(std::fstream& stream) {
  const std::size_t length = strlen(MORKATO_SIGNATURE);
  char signature[length + 1];
  char empty;
  signature[length] = '\0';
  stream.read(signature, length);
  stream.read(&empty, sizeof(char));
  return (stream.good() && strcmp(MORKATO_SIGNATURE, signature) == 0 && empty == '\0');
}