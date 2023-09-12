from morkato  import MorkatoBot
from decouple import config

from sys import exit

import dotenv

def main() -> int:
  dotenv.load_dotenv()
  
  try:
    TOKEN: str = config('BOT_TOKEN')
  except:
    print('Insira no ".env" uma chave chamada: BOT_TOKEN com seu token do discord.')

    return -1

  bot = MorkatoBot(auth=TOKEN)
  
  bot.run(TOKEN)
  
  return 0

if __name__ == '__main__':
  exit(main())
