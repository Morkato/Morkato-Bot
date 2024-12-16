from __future__ import annotations
from discord.ext.commands.bot import Bot
from discord.ext.commands.errors import (
  CommandError,
  CommandInvokeError,
  ConversionError
)
from .extension import (ErrorCallback, Extension, Converter)
from .core import (MorkatoCommandTree, MessageBuilder, BotBuilder)
from .context import MorkatoContext
from types import ModuleType
from typing import (
  Optional,
  TypeVar,
  Type,
  Dict,
  Any
)
import importlib.util
import discord.utils
import discord
import logging
import asyncio
import sys
import os

_log = logging.getLogger(__name__)
T = TypeVar('T')
class MorkatoBot(Bot):
  def __init__(
    self, *args,
    msgbuilder: MessageBuilder,
    extensions: Dict[str, Extension],
    converters: Dict[Type[Any], Converter[Any]],
    catching: Dict[Type[Any], ErrorCallback],
    injected: Dict[Type[Any], Any],
    **kwargs
  ) -> None:
    tree_cls = kwargs.pop("tree_cls", None)
    if tree_cls is None:
      tree_cls = MorkatoCommandTree
    super().__init__(
      *args,
      **kwargs,
      tree_cls=tree_cls
    )
    self.msgbuilder = msgbuilder
    self.morkextensions = extensions
    self.morkconverters = converters
    self.morkcatching = catching
    self.injected = injected
  async def get_context(self, message: discord.Message, /) -> MorkatoContext:
    return await super().get_context(message, cls=MorkatoContext)
  async def on_ready(self) -> None:
    await self.tree.sync()
    _log.info("Estou conectado, como: %s" % self.user.name)
  async def on_command_error(self, context: MorkatoContext, exception: CommandError) -> None:
    base_exception: Optional[Exception] = None
    if isinstance(exception, (CommandInvokeError, ConversionError)):
      base_exception = exception.original
    exc_cls = type(exception)
    callback = self.morkcatching.get(exc_cls)
    if callback is not None:
      await callback.invoke(context, exception)
      return
    if base_exception is None:
      return await super().on_command_error(context, exception)
    base_exc_cls = type(base_exception)
    callback = self.morkcatching.get(base_exc_cls)
    if callback is None:
      try:
        catching = (callback for (cls, callback) in self.morkcatching.items() if issubclass(base_exc_cls, cls))
        callback = next(catching)
      except StopIteration:
        return await super().on_command_error(context, exception)
    await callback.invoke(context, base_exception)
  def inject(self, cls: Type[T], object: T, /) -> None:
    self.injected[cls] = object

async def amain(builder: BotBuilder, bot: MorkatoBot, token: str) -> None:
  async with bot:
    await bot.login(token)
    await builder.setup(bot)
    await bot.connect()
def main(class_location: Optional[str] = None, *argv) -> int:
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
    return 1
  if PREFIX is None:
    print("O campo \"BOT_PREFIX\" é requerido.")
    return 1
  if BOT_TOKEN is None:
    print("O campo \"BOT_TOKEN\" é requerido.")
    return 1
  sys.path.append(os.path.abspath(MORKATO_HOME))
  discord.utils.setup_logging(
    root=True
  )
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
  print("Entry Class: %s.%s" % (cls.__module__, cls.__name__))
  msgbuilder = MessageBuilder(os.path.join(MORKATO_HOME, "content"))
  builder = BotBuilder(msgbuilder, MORKATO_HOME, discord.Intents.all())
  builder.command_prefix(PREFIX)
  builder.prepare()
  bot = builder.login(cls)
  try:
    asyncio.run(amain(builder, bot, BOT_TOKEN))
  except KeyboardInterrupt:
    pass
  return 0
if __name__ == "__main__":
  argv = sys.argv[2:]
  exit(main(*argv))