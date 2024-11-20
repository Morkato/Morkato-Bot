#include <iostream>
#include "morkato/repository.cpp"
#include "morkato/storage.cpp"
#include "morkato/uuid.cpp"
#include <ctime>
#include <fstream>

const char* morkato_work_dir;

void morkInit() {
  morkato_work_dir = ".morkato";
}
void morkClose() {
  
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

int main() {
  morkInit();
  // size_t size;
  // void* file = readFile("/home/evaristo/Pictures/Mitsuri_shows_how_she_sheathes_her_katana.gif", &size);
  // saveObject(&file, size);
  // free(file);
  // size_t length = 0;
  // char* data = getObject(0, &length);
  // std::ofstream file("abc.gif", std::ios::binary);
  // file.write(data, length);
  MorkatoRepository* a;
  morkRepository(a, nullptr, 0);
  morkClose();
  return 0;
}