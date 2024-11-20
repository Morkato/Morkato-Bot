#pragma once
#include <iostream>
#include <algorithm>
#include <string.h>
#include <filesystem>
#include <fstream>
#include <string>
#define REPOSITORY_SPECIAL_FILE ".mkr"
#define REPOSITORY_SPECIAL_FILE_LENGTH strlen(REPOSITORY_SPECIAL_FILE)
#ifndef MORKATO_SIGNATURE
#define MORKATO_SIGNATURE "MORKATO"
#define MORKATO_CHUNKER_LENGTH_MAX ((1 << 32) - 2)
#define MORKATO_CHUNKER_SIZE_MAX ((1 << 32) - 2)
#endif
typedef struct {
  size_t size;
  size_t length;
} MorkatoChunker;
extern const char* morkato_work_dir;
void mkdirIfNotExists(const char* path) {
  namespace fs = std::filesystem;
  if (fs::exists(path)) {
    if (!fs::is_directory(path))
      throw new std::runtime_error("");
    return;
  }
  fs::create_directory(path);
}
void morkGetChunkerLocation(const char* reps, char chunker, size_t* size, size_t* length) {
  *length = MORKATO_CHUNKER_LENGTH_MAX + 1;
  *size = MORKATO_CHUNKER_SIZE_MAX + 1;
  namespace fs = std::filesystem;
  std::string filepath = morkato_work_dir;
  mkdirIfNotExists(filepath.c_str());
  filepath += "/repositories";
  mkdirIfNotExists(filepath.c_str());
  filepath += '/';
  const char* final_ptr = reps + strlen(reps);
  for (const char* repo_id = reps; repo_id!=final_ptr; ++repo_id) {
    std::string repr = std::to_string(static_cast<uint>(*repo_id));
    filepath += repr;
    if (!fs::exists(filepath)) {
      return;
    }
    filepath += '/';
  }
  filepath += REPOSITORY_SPECIAL_FILE;
  if (!fs::exists(filepath)) {
    return;
  }
  std::ifstream file(filepath, std::ios::binary);
  char* signature;
  file.read(signature, strlen(MORKATO_SIGNATURE));
  if (strcmp(MORKATO_SIGNATURE, signature) != 0) {
    return;
  }
  size_t repo_length = 0;
  file.read(reinterpret_cast<char*>(&repo_length), sizeof(size_t));
  if (chunker >= repo_length) {
    return;
  }
  file.seekg(sizeof(size_t), std::ios::beg);
  file.seekg(sizeof(MorkatoChunker) * chunker, std::ios::cur);
  MorkatoChunker chunk;
  file.read(reinterpret_cast<char*>(&chunker), sizeof(MorkatoChunker));
  *size = chunk.size;
  *length = chunk.length;
}