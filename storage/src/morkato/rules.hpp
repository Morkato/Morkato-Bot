#pragma once
#include <iostream>
#include <stdint.h>
#define MORKATO_REPOSITORY_SPECIAL_FILE "repository.morkr"
#define MORKATO_PATH_PREFIX "morkp"
#define MORKATO_CHUNKER_SIZE_MAX __SIZE_MAX__
#define MORKATO_TEMPORARY_FILE_SULFIX ".morktmp"
#define MORKATO_CHUNKER_SULFIX ".morkc"
#define MORKATO_SIGNATURE "MORKATO"
#define MORKATO_LENGTH_MAX 0xff
#define morkForLoopSig(__t, __k, __v) \
  for (__t __k = 0; __k < __v; ++__k)
#define morkForLoop(__k, __v) morkForLoopSig(std::size_t, __k, __v)
typedef struct __attribute__((packed)) {
  uint8_t subrepositories_length = 0;
  uint8_t chunks_length = 0;
} morkrepository;
typedef struct __attribute__((packed)) {
  uint8_t length = 0;
  std::size_t size = 0;
} morkchunker;
typedef struct __attribute__((packed)) {
  std::size_t location;
  std::size_t length;
} morkchunk;
void morkCreateRepositoryFile(std::fstream& stream);
bool morkValidateSignature(std::fstream& stream);
void morkCreateChunkFile(std::fstream& stream);