#include "morkato/repository.cpp"
#include "morkato/settings.cpp"
#include "morkato/streams.cpp"
#include "morkato/storage.cpp"
#include "morkato/rules.cpp"
#include <iostream>
#include <chrono>

const char* readFile(const char* filepath, size_t* size) {
  std::ifstream file(filepath, std::ios::binary | std::ios::ate);
  *size = file.tellg();
  file.seekg(0, std::ios::beg);
  char* buffer = new char[*size];
  file.read(buffer, *size);
  file.close();
  return buffer;
}

int main() {
  morksettings settings;
  settings.morkbuf_length = 1024 * 1024 * 12; // 12MB (RAM)
  morkStorageInit(settings);

  auto start = std::chrono::high_resolution_clock::now();

  morkistream stream(reinterpret_cast<const uint8_t*>(""), 0, 0, 40);
  if (!stream.success()) {
    std::cerr << "Erro!" << std::endl;
    return 1;
  }
  std::cout << "Size: " << stream.size() << std::endl;
  std::ofstream file("test.gif", std::ios::app | std::ios::binary);
  char* buffer = new char[stream.size()];
  stream.read(buffer, stream.size());
  file.write(buffer, stream.size());

  // size_t size;
  // const char* buffer = readFile("/home/evaristo/Pictures/Mitsuri_shows_how_she_sheathes_her_katana.gif", &size);
  // morkostream stream(size);
  // stream.write(buffer, size);

  auto end = std::chrono::high_resolution_clock::now();
  file.close();
  auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();
  std::cout << "Duration: " << duration << "ms" << std::endl;
  morkStorageClose();
  return 0;
}