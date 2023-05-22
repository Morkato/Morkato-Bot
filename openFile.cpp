#include <iostream>
#include <fstream>

int main(int argc, char *argv[])
{
  if (argc != 2)
  {
    std::cerr << "Usage: ./program <filename>" << std::endl;
    return 1;
  }

  const char *filename = argv[1];

  std::ifstream file(filename);
  if (!file)
  {
    std::cerr << "Failed to open file: " << filename << std::endl;
    return 1;
  }

  std::string line;
  while (std::getline(file, line))
  {
    std::cout << line << std::endl;
  }

  file.close();

  return 0;
}
