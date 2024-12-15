#pragma once
#include <fstream>
class morkostream {
  private:
    const std::streamsize size;
    std::fstream stream;
    std::streamsize current_size;
    bool is_success;
  public:
    morkostream(const std::size_t size);
    ~morkostream();
    bool write(const char* buffer, std::streamsize size);
    bool success();
    void flush();
    void destroy();
};
class morkistream {
  private:
    std::streamsize _size;
    std::fstream stream;
    std::streamsize cur;
    bool is_success;
  public:
    morkistream(const uint8_t* repositories, const size_t repositories_length, const uint8_t chunker, const uint8_t location);
    ~morkistream();
    bool read(char* buffer, const std::streamsize size);
    const std::size_t size();
    bool success();
    void destroy();
};