#include <boost/asio.hpp>
#include <boost/asio/awaitable.hpp>
#include <boost/asio/use_awaitable.hpp>
#include <boost/asio/co_spawn.hpp>
#include <boost/asio/detached.hpp>
#include <memory>
class morksocket {
  public:
    morksocket(boost::asio::io_context& io, int id);
    ~morksocket();
    boost::asio::awaitable<int> read(char* buffer, size_t size);
    boost::asio::awaitable<int> write(const char* buffer, size_t size);
    boost::asio::awaitable<void> run();
    void close();
  private:
    boost::asio::ip::tcp::socket sock;
    boost::asio::io_context& io;
    bool is_running;
    int id;
};