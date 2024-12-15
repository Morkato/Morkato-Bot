#pragma once
#include "./repository.hpp"
#include "./rules.cpp"
#include <glob.h> // glob(), globfree()
#include <string.h>
#include <iostream>
#include <string.h>
#include <string>
extern const char* MORKATO_STORAGE_LOCATION;

bool morkGetChunkerMetadata(const uint8_t* repositories, const size_t length, const uint8_t chunkerIndex, morkchunker* chunker) {
  namespace fs = std::filesystem;
  fs::path entry(MORKATO_STORAGE_LOCATION);
  morkForLoop(idx, length) {
    entry /= fs::path(std::to_string(repositories[idx]));
  }
  std::fstream file(entry / fs::path(MORKATO_REPOSITORY_SPECIAL_FILE));
  if (!file.is_open() || !morkValidateSignature(file)) {
    file.close();
    return false;
  }
  morkrepository metadata;
  morkReadMetadata(&metadata, file);
  if (chunkerIndex >= metadata.chunks_length || !file.good()) {
    file.close();
    return false;
  }
  file.seekg(sizeof(morkchunker) * chunkerIndex, std::ios::cur);
  file.read(reinterpret_cast<char*>(chunker), sizeof(morkchunker));
  if (!file.good()) {
    file.close();
    return false;
  }
  file.close();
  return true;
}
bool morkGetChunkerBySize(const std::streamsize size, std::filesystem::path* entry, morkchunker* chunker, uint8_t* index) {
  namespace fs = std::filesystem;
  fs::path filepath = *entry / fs::path(MORKATO_REPOSITORY_SPECIAL_FILE);
  std::fstream file;
  if (!fs::exists(filepath)) {
    file.open(filepath, std::ios::out | std::ios::binary);
    morkCreateRepositoryFile(file);
    file.close();
  }
  file.open(filepath, std::ios::in | std::ios::out | std::ios::binary);
  if (!file.is_open() || !morkValidateSignature(file)) {
    std::cerr << "Falha ao abrir o arquivo, no tamanho estátio ou na validação de assinatura." << std::endl;
    file.close();
    return false;
  }
  morkrepository repository;
  morkReadMetadata(&repository, file);
  if (!file.good()) {
    return false;
  }
  morkForLoop(i, repository.chunks_length) {
    file.read(reinterpret_cast<char*>(chunker), sizeof(morkchunker));
    if (chunker->length < MORKATO_LENGTH_MAX && chunker->size <= MORKATO_CHUNKER_SIZE_MAX && size <= chunker->size) {
      *index = i;
      file.close();
      return true;
    }
  }
  if (repository.chunks_length < MORKATO_LENGTH_MAX) {
    *index = repository.chunks_length;
    ++repository.chunks_length;
    morkUpdateRepositoryMetadata(&repository, file);
    file.close();
    return true;
  }
  if (repository.subrepositories_length < MORKATO_LENGTH_MAX) {
    *entry = *entry / fs::path(std::string(MORKATO_PATH_PREFIX) + std::to_string(repository.subrepositories_length));
    if (fs::exists(*entry)) {
      file.close();
      return false;
    }
    ++repository.subrepositories_length;
    morkUpdateRepositoryMetadata(&repository, file);
    file.close();
    fs::create_directory(*entry);
    fs::path filepath = *entry / fs::path(MORKATO_REPOSITORY_SPECIAL_FILE);
    file.open(filepath, std::ios::out | std::ios::binary);
    morkCreateRepositoryFile(file);
    file.close();
    return true;
  }
  file.close();
  morkrepository choicedRepository{MORKATO_LENGTH_MAX,MORKATO_LENGTH_MAX};
  uint8_t choicedRepositoryId = MORKATO_LENGTH_MAX;
  morkForLoopSig(uint8_t, subdirectory, repository.subrepositories_length) {
    fs::path filepath = *entry / fs::path(std::string(MORKATO_PATH_PREFIX) + std::to_string(subdirectory)) / fs::path(MORKATO_REPOSITORY_SPECIAL_FILE);
    file.open(filepath, std::ios::in | std::ios::binary);
    if (!morkValidateSignature(file)) {
      file.close();
      return false;
    }
    morkrepository other;
    morkReadMetadata(&other, file);
    file.close();
    if (choicedRepository.subrepositories_length > other.subrepositories_length) {
      choicedRepository = other;
      choicedRepositoryId = subdirectory;
    }
  }
  *entry = *entry / fs::path(std::string(MORKATO_PATH_PREFIX) + std::to_string(choicedRepositoryId));
  return morkGetChunkerBySize(size, entry, chunker, index);
}