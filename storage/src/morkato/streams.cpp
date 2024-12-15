#pragma once
#include <filesystem>
#include <iostream>
#include <vector>
#include "./repository.cpp"
#include "./streams.hpp"
#include "./rules.cpp"

extern const char* MORKATO_STORAGE_LOCATION;
extern const char* MORKATO_TMP_LOCATION;
extern std::vector<char> MORKATO_ZEROS;
extern std::size_t MORKATO_BUFFER_LENGTH;

morkostream::morkostream(const std::size_t size) : size(size), current_size(0), is_success(false) {
  namespace fs = std::filesystem;
  std::filesystem::path entry(MORKATO_STORAGE_LOCATION);
  uint8_t chunker_index;
  morkchunker chunker;
  bool success = morkGetChunkerBySize(size, &entry, &chunker, &chunker_index);
  if (!success) {
    std::cerr << "Nenhum chunker foi encontrado, será um erro?" << std::endl;
    return;
  }
  morkchunk chunk {chunker.size, size};
  fs::path chunkerFilepath = entry / (std::to_string(chunker_index) + std::string(MORKATO_CHUNKER_SULFIX));
  if (!fs::exists(chunkerFilepath)) {
    stream.open(chunkerFilepath, std::ios::out | std::ios::binary);
    morkCreateChunkFile(stream);
    stream.close();
  }
  stream.open(entry / fs::path(MORKATO_REPOSITORY_SPECIAL_FILE), std::ios::in | std::ios::out | std::ios::binary);
  if (!stream.is_open() || !morkValidateSignature(stream)) {
    return;
  }
  uint8_t position = chunker.length;
  chunker.size += size;
  ++chunker.length;
  morkrepository repository;
  morkReadMetadata(&repository, stream);
  stream.seekp(sizeof(morkchunker) * chunker_index, std::ios::cur);
  stream.write(reinterpret_cast<const char*>(&chunker), sizeof(morkchunker));
  if (!stream.good()) {
    stream.close();
    return;
  }
  stream.close();
  stream.open(chunkerFilepath, std::ios::in | std::ios::out | std::ios::binary);
  if (!stream.is_open() || !morkValidateSignature(stream)) {
    return;
  }
  std::streampos offset = stream.tellg();
  stream.seekp(sizeof(morkchunk) * position, std::ios::cur);
  stream.write(reinterpret_cast<const char*>(&chunk), sizeof(morkchunk));
  stream.seekp(offset, std::ios::beg);
  stream.seekp(sizeof(morkchunk) * MORKATO_LENGTH_MAX, std::ios::cur);
  stream.seekp(sizeof(char), std::ios::cur);
  stream.seekp(sizeof(char) * chunk.location, std::ios::cur);
  offset = stream.tellp();
  std::size_t dataRestZeros = size % MORKATO_BUFFER_LENGTH;
  std::size_t zerosQuantity = (size - dataRestZeros) / MORKATO_BUFFER_LENGTH;
  stream.write(MORKATO_ZEROS.data(), dataRestZeros);
  morkForLoop(i, zerosQuantity) {
    stream.write(MORKATO_ZEROS.data(), MORKATO_BUFFER_LENGTH);
  }
  stream.seekp(offset, std::ios::beg);
  is_success = true;
}
morkostream::~morkostream() {
  destroy();
}
bool morkostream::success() {
  return is_success;
}
bool morkostream::write(const char* buffer, std::streamsize size) {
  if (this->current_size + size > this->size || !stream.is_open()) {
    return false;
  }
  stream.write(buffer, size);
  if (!stream.good()) {
    return false;
  }
  current_size += size;
  return true;
}
void morkostream::flush() {
  if (success() && stream.is_open() && stream.good()) {
    stream.flush();
  }
}
void morkostream::destroy() {
  if (stream) {
    stream.close();
  }
}

morkistream::morkistream(const uint8_t* repositories, const size_t repositories_length, const uint8_t index, const uint8_t location) : cur(0), is_success(false) {
  namespace fs = std::filesystem;
  morkchunker chunker;
  bool success = morkGetChunkerMetadata(repositories, repositories_length, index, &chunker);
  if (!success || location >= chunker.length) {
    return;
  }
  fs::path entry(MORKATO_STORAGE_LOCATION);
  morkForLoop(idx, repositories_length) {
    entry /= fs::path(std::to_string(repositories[idx]));
  }  
  entry /= fs::path(std::to_string(index) + std::string(MORKATO_CHUNKER_SULFIX));
  stream.open(entry, std::ios::in | std::ios::binary);
  morkchunk chunk;
  if (!stream.is_open() || !morkValidateSignature(stream)) {
    stream.close();
    return;
  }
  std::streampos offset = stream.tellg();
  stream.seekg(offset, std::ios::beg);
  stream.seekg(sizeof(morkchunk) * location, std::ios::cur);
  stream.read(reinterpret_cast<char*>(&chunk), sizeof(morkchunk));
  if (!stream.good()) {
    stream.close();
    return;
  }
  stream.seekg(offset, std::ios::beg);
  stream.seekg(sizeof(morkchunk) * MORKATO_LENGTH_MAX, std::ios::cur);
  char empty = '\0';
  stream.read(&empty, sizeof(char));
  if (!stream.good() || empty != '\0') {
    std::cerr << "Chunker Invalido." << std::endl;
    stream.close();
    return;
  }
  stream.seekg(chunk.location, std::ios::cur);
  _size = chunk.length;
  is_success = true;
}
morkistream::~morkistream() {
  destroy();
}
bool morkistream::success() {
  return is_success;
}
const std::size_t morkistream::size() {
  return _size;
}
void morkistream::destroy() {
  if (stream.is_open()) {
    stream.close();
  }
}
bool morkistream::read(char* buffer, const std::streamsize size) {
  if (this->cur + size > this->_size || !stream.is_open()) {
    return false;
  }
  stream.read(buffer, size);
  if (!stream.good()) {
    return false;
  }
  cur += size;
  return true;
}