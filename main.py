from morkato.client import Client
from decouple       import config

from sys import exit

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s : %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

def main() -> int:
  try:
    TOKEN: str = config('BOT_TOKEN')
  except:
    print('Insira no ".env" uma chave chamada: BOT_TOKEN com seu token do discord.')

    return -1

  bot = Client(auth=TOKEN)
  
  bot.run(TOKEN)
  
  return 0

if __name__ == '__main__':
  exit(main())
