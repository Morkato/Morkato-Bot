#include "morkato/repository.cpp"
#include "morkato/settings.cpp"
#include "morkato/streams.cpp"
#include "morkato/storage.cpp"
#include "morkato/socket.cpp"
#include "morkato/rules.cpp"
#include <iostream>

#define BUFFER_SIZE 1024
#define PORT 7891

int main() {
  morkservsettings settings;
  settings.morkserv_port = PORT;
  settings.morkserv_peer = 1024;
  int status = morkInetInit(settings);
  if (status != 0) {
    std::cout << "Error!" << std::endl;
    return EXIT_FAILURE;
  }
  std::cout << "Conexão efetuada!" << std::endl;
  int conn = morkAcceptConnection();
  std::cout << "Conection: " << conn << std::endl;
  close(conn);
  morkInetClose();
  return EXIT_SUCCESS;
}