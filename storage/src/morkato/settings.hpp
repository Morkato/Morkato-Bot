#pragma once
#include <iostream>
#include <stdint.h>
struct morksettings {
  char* morkstorage_location = "./storage";
  char* morktmp_location = "./tmp";
  std::size_t morkbuf_length = (1024 * 4);
};
struct morkservsettings {
  uint16_t morkserv_port;
  uint32_t morkserv_peer;
};