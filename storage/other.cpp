#include <iostream>
#include <fstream>
#include "morkato/rules.cpp"
void morkRepositoryConsoleWrite(std::fstream& stream) {
  if (!morkValidateSignature(stream)) {
    std::cout << "Invalid stream signature." << std::endl;
    return;
  }
  morkrepository metadata;
  stream.read(reinterpret_cast<char*>(&metadata), sizeof(morkrepository));
  std::cout << "Metadata:" << std::endl;
  std::cout << "Chunks Length: " << std::to_string(metadata.chunks_length) << std::endl;
  std::cout << "Subdirectories Length: " << std::to_string(metadata.subrepositories_length) << std::endl;
  morkForLoopSig(uint8_t, i, metadata.chunks_length) {
    std::cout << "Chunk (" << std::to_string(i) << "): " << std::endl;
    morkchunker chunker;
    stream.read(reinterpret_cast<char*>(&chunker), sizeof(morkchunker));
    std::cout << "Size: " << std::to_string(chunker.size) << std::endl;
    std::cout << "Length: " << std::to_string(chunker.length) << std::endl;
  }
}
int main() {
  std::fstream stream("storage/repository.morkr", std::ios::binary | std::ios::in);
  morkRepositoryConsoleWrite(stream);
  std::cout << std::endl;
  stream.close();
  stream.open("storage/0.morkc", std::ios::binary | std::ios::in);
  morkValidateSignature(stream);
  morkchunk chunk;
  stream.read(reinterpret_cast<char*>(&chunk), sizeof(morkchunk));
  std::cout << "Length: " << chunk.length << " Location: " << chunk.location << std::endl;
  stream.read(reinterpret_cast<char*>(&chunk), sizeof(morkchunk));
  std::cout << "Length: " << chunk.length << " Location: " << chunk.location << std::endl;
  stream.read(reinterpret_cast<char*>(&chunk), sizeof(morkchunk));
  std::cout << "Length: " << chunk.length << " Location: " << chunk.location << std::endl;
  stream.read(reinterpret_cast<char*>(&chunk), sizeof(morkchunk));
  std::cout << "Length: " << chunk.length << " Location: " << chunk.location << std::endl;
  stream.close();
  return 0;
}


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
}
void morkStorageClose() {
  MORKATO_ZEROS.clear();
  MORKATO_ZEROS.shrink_to_fit();
}

void* readFile(const char* filepath, size_t* size) {
  std::ifstream file(filepath, std::ios::binary | std::ios::ate);
  *size = file.tellg();
  file.seekg(0, std::ios::beg);
  void* buffer = malloc(*size);
  file.read(reinterpret_cast<char*>(buffer), *size);
  file.close();
  return buffer;
}

void morkRepositoryConsoleWrite(std::fstream& stream) {
  if (!morkValidateSignature(stream)) {
    std::cout << "Invalid stream signature." << std::endl;
    return;
  }
  morkrepository metadata;
  stream.read(reinterpret_cast<char*>(&metadata), sizeof(morkrepository));
  std::cout << "Metadata:" << std::endl;
  std::cout << "Chunks Length: " << std::to_string(metadata.chunks_length) << std::endl;
  std::cout << "Subdirectories Length: " << std::to_string(metadata.subrepositories_length) << std::endl;
  morkForLoopSig(uint8_t, i, metadata.chunks_length) {
    std::cout << "Chunk (" << std::to_string(i) << "): " << std::endl;
    morkchunker chunker;
    stream.read(reinterpret_cast<char*>(&chunker), sizeof(morkchunker));
    std::cout << "Size: " << std::to_string(chunker.size) << std::endl;
    std::cout << "Length: " << std::to_string(chunker.length) << std::endl;
  }
}

// int main() {
//   morkInit();
//   // size_t size;
//   // void* buffer = readFile("./test2.gif", &size);
//   // morkostream stream(size);
//   // if (!stream.success()) {
//   //   std::cerr << "Ocorreu um erro." << std::endl;
//   //   return 1;
//   // }
//   // stream.write(reinterpret_cast<const char*>(buffer), size);
//   const uint8_t* repositories = new uint8_t[1] {0};
//   morkistream stream(repositories, 0, 0, 3);
//   std::cout << stream.size() << std::endl;
//   std::ofstream out("t5.gif", std::ios::binary);
//   char* buffer = new char[stream.size()];
//   stream.read(buffer, stream.size());
//   out.write(buffer, stream.size());
//   stream.destroy();
//   // morkostream stream(12);
//   // stream.write("M", 1);
//   // stream.write("O", 1);
//   // stream.write("R", 1);
//   // stream.write("K", 1);
//   // stream.write("A", 1);
//   // stream.write("T", 1);
//   // stream.write("O", 1);
//   // stream.write("!", 1);
//   // stream.write("A", 1);
//   // stream.write("B", 1);
//   morkClose();
//   return 0;
// }

// int main() {
//   morksettings settings;
//   settings.morkbuf_length = 1024 * 1024 * 12; // 12MB (RAM)
//   morkStorageInit(settings);

//   // size_t size;
//   // const char* buffer = readFile("/home/evaristo/Pictures/Mitsuri_shows_how_she_sheathes_her_katana.gif", &size);
//   // morkostream stream(size);
//   // stream.write(buffer, size);
//   auto start = std::chrono::high_resolution_clock::now();

//   morkistream stream(reinterpret_cast<const uint8_t*>(""), 0, 0, 5);
//   if (!stream.success()) {
//     std::cerr << "Erro!" << std::endl;
//     return 1;
//   }
//   std::cout << "Size: " << stream.size() << std::endl;
//   std::ofstream file("test.gif", std::ios::app | std::ios::binary);
//   char* buffer = new char[stream.size()];
//   stream.read(buffer, stream.size());
//   file.write(buffer, stream.size());

//   auto end = std::chrono::high_resolution_clock::now();
//   auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();
//   std::cout << "Duration: " << duration << "ms" << std::endl;
//   morkStorageClose();
//   return 0;
// }