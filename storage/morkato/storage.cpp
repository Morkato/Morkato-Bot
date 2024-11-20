#pragma once
#include <iostream>
#include <fstream>
#include <string.h>
#include <cstring>

#define SIGNATURE "MORKATO"
#define SIGNATURE_LENGTH strlen(SIGNATURE)
#define isSignature(__v) strcmp(SIGNATURE, __v) == 0

extern const char* morkato_work_dir;

typedef struct {
  size_t location;
  size_t length;
} Chunk;

void saveObject(void** obj, size_t& size) {
  std::ofstream file("test.bin", std::ios::binary);
  size_t length = 1;
  Chunk* chunks = (Chunk*)malloc(sizeof(Chunk) * length);
  chunks[0] = {0, size};
  file << SIGNATURE;
  file.write(reinterpret_cast<const char*>(&size), sizeof(size_t));
  file.write(reinterpret_cast<const char*>(&length), sizeof(size_t));
  file.write(reinterpret_cast<const char*>(chunks), sizeof(Chunk) * length);
  file.write(reinterpret_cast<const char*>(*obj), size);
  file.close();
}
char* morkGetObject(char* reps, char chumker, size_t location, size_t* size) {
  size_t chunker_length;
  std::ifstream file("test.bin", std::ios::binary);
  char* signature = (char*)malloc(sizeof(char) * SIGNATURE_LENGTH);
  file.read(signature, sizeof(char) * SIGNATURE_LENGTH);
  if (!isSignature(signature)) {
    std::cout << signature << '\n';
    return nullptr;
  }
  size_t arq_size;
  size_t length;
  file.read(reinterpret_cast<char*>(&arq_size), sizeof(size_t));
  file.read(reinterpret_cast<char*>(&length), sizeof(size_t));
  if (location >= length) {
    return nullptr;
  }
  file.seekg(SIGNATURE_LENGTH + 2 * sizeof(size_t), std::ios::beg);
  file.seekg(sizeof(Chunk) * location, std::ios::cur);
  Chunk chunk;
  file.read(reinterpret_cast<char*>(&chunk), sizeof(Chunk));
  std::cout << "Chunk: location = " << chunk.location << ", length = " << chunk.length << std::endl;
  *size = chunk.length;
  file.seekg(SIGNATURE_LENGTH + 2 * sizeof(size_t) + length * sizeof(Chunk), std::ios::beg);
  char* result = new char[chunk.length];
  file.read(result, chunk.length);
  file.close();
  return result;
}