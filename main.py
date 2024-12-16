from morkbmt.core import (BotBuilder, MessageBuilder)
from morkbmt.bot import MorkatoBot
from discord.flags import Intents
from types import ModuleType
from typing import (
  Optional,
  Type
)
import importlib.util
import discord.utils
import asyncio
import sys
import os

async def amain(builder: BotBuilder, bot: MorkatoBot, token: str) -> None:
  async with bot:
    await bot.login(token)
    await builder.setup(bot)
    await bot.connect()
def main(token: str, class_location: Optional[str] = None, *argv) -> int:
  cls: Type[MorkatoBot] = MorkatoBot
  if class_location is not None:
    (module_name, cls_name) = class_location.rsplit('.', 1)
    module = sys.modules.get(module_name)
    if module is None:
      module = ModuleType(module_name)
      spec = importlib.util.find_spec(module_name)
      if spec is None or spec.loader is None:
        print("Module: %s is notfound." % module_name)
        return 1
      spec.loader.exec_module(module)
      sys.modules[module_name] = module
    cls = getattr(module, cls_name, None)
    if cls is None:
      print("Class: %s is notfound in module: %s." % (cls_name, module_name))
      return 1
    if not issubclass(cls, MorkatoBot):
      print("Class: %s in module: %s is not subclass of: %s.%s." % (cls_name, module_name, MorkatoBot.__module__, MorkatoBot.__name__))
      return 1
  msgbuilder = MessageBuilder(os.path.join(MORKATO_HOME, "content"))
  builder = BotBuilder(msgbuilder, MORKATO_HOME, Intents.all())
  builder.command_prefix(PREFIX)
  builder.prepare()
  bot = builder.login(cls)
  try:
    asyncio.run(amain(builder, bot, token))
  except KeyboardInterrupt:
    pass
  return 0
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
  exit(main(BOT_TOKEN, *sys.argv[1:]))