from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from sys import _ExitCode

def main() -> '_ExitCode':
  load_dotenv()
  setup_logging()

  BOT_TOKEN = os.getenv('BOT_TOKEN')
  MORKATO_TOKEN = os.getenv('MTK_TOKEN')
  DEV_PATTERN = os.getenv('DEV_PATTERN')

  if BOT_TOKEN is None:
    print('Forneça um token do discord. (BOT_TOKEN)')

    return 1
  
  if MORKATO_TOKEN is None:
    print('Forneça um token da api mkt. (MTK_TOKEN)')
    
    return 1
  
  bot = MorkatoBot(['!', 'dev!'], MORKATO_TOKEN, re.compile(DEV_PATTERN or r'^dev'))

  bot.run(BOT_TOKEN)

  return 0

if __name__ == '__main__':
  from morkato.utils.logging import setup_logging
  from dotenv                import load_dotenv
  from morkato.bot           import MorkatoBot

  import re
  import os
  
  exit(main())

def main() -> '_ExitCode':
  return 0