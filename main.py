from morkato.work.builder import MessageBuilder
from morkato.work.project import BotBuilder
from discord.flags import Intents
from app.bot import AppBot
import discord.utils
import asyncio
import sys
import os

async def amain(builder: BotBuilder, token: str) -> None:
  bot = builder.login(AppBot)
  async with bot:
    await bot.login(token)
    await builder.setup(bot)
    await bot.connect()
def main(builder: BotBuilder, token: str) -> None:
  try:
    asyncio.run(amain(builder, token))
  except KeyboardInterrupt:
    pass
if __name__ == "__main__":
  try:
    from dotenv import load_dotenv
    load_dotenv()
  except ModuleNotFoundError:
    pass
  MORKATO_HOME = os.getenv("MORKATO_HOME")
  BOT_TOKEN = os.getenv("BOT_TOKEN")
  PREFIX = os.getenv("BOT_PREFIX")
  if MORKATO_HOME is None:
    print("MORKATO_HOME is undefined.")
    exit(1)
  if PREFIX is None:
    print("O campo \"BOT_PREFIX\" é requerido.")
    exit(1)
  if BOT_TOKEN is None:
    print("O campo \"BOT_TOKEN\" é requerido.")
    exit(1)
  sys.path.append(os.path.abspath(MORKATO_HOME))
  discord.utils.setup_logging(
    root=True
  )
  msgbuilder = MessageBuilder(os.path.join(MORKATO_HOME, "content"))
  builder = BotBuilder(msgbuilder, MORKATO_HOME, Intents.all())
  builder.command_prefix(PREFIX)
  builder.from_home()
  main(builder, BOT_TOKEN)