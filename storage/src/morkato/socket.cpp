#pragma once
#include "./settings.cpp"
#include "./socket.hpp"
#include <sys/socket.h>
#include <netinet/in.h>
#include <cstring>
#include <iostream>
#include <unistd.h>
#include <stdint.h>
#include <thread>

uint16_t MORKATO_SERVER_PORT;
uint32_t MORKATO_SERVER_PEER;
uint32_t MORKATO_SERVER_CLIENTS_COUNT;
sockaddr_in MORKATO_SERVER_ADDRESS;
int MORKATO_SERVER_FD;
bool MORKATO_SERVER = false;

int morkInetInit(const morkservsettings& settings) {
  MORKATO_SERVER_PORT = settings.morkserv_port;
  MORKATO_SERVER_PEER = settings.morkserv_peer;
  MORKATO_SERVER_CLIENTS_COUNT = 0;
  int option = 1;
  sockaddr_in address;
  std::size_t addrlen = sizeof(address);
  int fd = socket(AF_INET, SOCK_STREAM, 0);
  if (fd == 0) {
    std::cerr << "Socket failed" << std::endl;
    return -1;
  }
  if (setsockopt(fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &option, sizeof(option))) {
    std::cerr << "setsockopt" << std::endl;
    close(fd);
    return -1;
  }
  address.sin_family = AF_INET;
  address.sin_addr.s_addr = INADDR_ANY;
  address.sin_port = htons(MORKATO_SERVER_PORT);
  int bind_status = bind(fd, (sockaddr*)&address, sizeof(address));
  if (bind_status < 0) {
    std::cerr << "Bind failed" << std::endl;
    close(fd);
    return -1;
  }
  int listen_status = listen(fd, 3);
  if (listen_status < 0) {
    std::cerr << "Listen failed" << std::endl;
    close(fd);
    return -1;
  }
  MORKATO_SERVER_ADDRESS = {address};
  MORKATO_SERVER_FD = fd;
  MORKATO_SERVER = true;
  return 0;
}
int morkAcceptConnection() {
  if (!MORKATO_SERVER) {
    return -2;
  }
  socklen_t addrlen = sizeof(MORKATO_SERVER_ADDRESS);
  int new_conn = accept(MORKATO_SERVER_FD, (sockaddr*)&MORKATO_SERVER_ADDRESS, &addrlen);
  if (new_conn < 0) {
    return -1;
  }
  return new_conn;
}
void morkRegistryClient() {
  
}
void morkInetClose() {
  close(MORKATO_SERVER_FD);
}

morksocket::morksocket(boost::asio::io_context& io, int id) : id(id), io(io), sock(io), is_running(true) {}