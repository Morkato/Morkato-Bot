from dotenv import load_dotenv
from app.bot import AppBot
import discord
import os

bot = AppBot(
  command_prefix='!',
  intents=discord.Intents.all(),
  base_message_builder="app/messages"
)
if __name__ == "__main__":
  load_dotenv()
  BOT_TOKEN = os.getenv("BOT_TOKEN")
  if BOT_TOKEN is None:
    exit(1)
  bot.run(BOT_TOKEN, root_logger=True)