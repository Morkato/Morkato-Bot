from decouple import config

from morkato.bot import Client

from sys import exit

def main() -> int:
  bot = Client()

  try:
    TOKEN: str = config('BOT_TOKEN')
  except:
    print('Insira no ".env" uma chave chamada: BOT_TOKEN com seu token do discord.')

    return -1

  bot.run(TOKEN)
  
  return 0

if __name__ == '__main__':
  exit(main())
