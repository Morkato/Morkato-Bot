#include <iostream>
#include <cstdlib>
#include <thread

int main()
{
  std::thread bot([]()
                  { std::system("python3 Index.py"); });
  std::thread backend([]()
                      { std::system("sudo yarn next:dev"); });

  backend.join();
  bot.join();

  return 0;
}