from morkato.ext.bot import MorkatoBot
from morkato.utils import load_modules
from dotenv import load_dotenv
import discord
import os

bot = MorkatoBot(
  command_prefix='!',
  intents=discord.Intents.all()
)
if __name__ == "__main__":
  load_dotenv()
  BOT_TOKEN = os.getenv("BOT_TOKEN")
  APP_DIR = os.getenv("APP_DIR") or "app"
  if BOT_TOKEN is None:
    exit(1)
  load_modules(APP_DIR)
  bot.run(BOT_TOKEN, root_logger=True)