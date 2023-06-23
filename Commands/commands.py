from typing import (Mapping, Sequence)
from discord.ext import commands
from types import ModuleType
from copy import deepcopy

import traceback
import re

class ImportPermissionError(Exception):
  def __init__(self, name: str) -> None:
    self.name: str = name

    super().__init__(f"Você não tem permissão para importar essa lib!")

def __load__(
  name: str,
  globals: Mapping[str, object] | None = ...,
  locals: Mapping[str, object] | None = ...,
  fromlist: Sequence[str] = ...,
  level: int = ...
) -> ModuleType:
  if name in ["socket", "requests",]:
    raise ImportPermissionError(name)
  return __import__(name, globals, locals, fromlist, level)

commandRegex = re.compile("```(?P<key>[A-Za-z0-9]+)\n(?P<code>[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ0-9.,\(\)/\"\'\\\^\:;!@#\$%&`\*\=\+\-\<\>~\[\]\{\}$?_\s]+)```")
importModules = {
  "__builtins__": {
    "__import__": __load__,
    "open": open,
    "True": True,
    "False": False,
    "str": str,
    "int": int,
    "bool": bool,
    "dict": dict,
    "tuple": tuple,
    "list": list,
    "enumerate": enumerate,
    "zip": zip,
    "getattr": getattr,
    "setattr": setattr,
    "__build_class__": __build_class__,
    "__name__": __name__,
    "property": property,
    "super": super,
    "type": type,
    "map": map,
    "next": next
  }
}

class Commands(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  @commands.command(name='console')
  async def Console(self, ctx: commands.Context, /, *, code: str) -> None:
    match = commandRegex.search(code)
    
    if match is None:
      await ctx.reply("**Não sei interpretar essa linguagem T-T**")
    
    elif match['key'] in [ 'py', 'python' ]:
      module = deepcopy(importModules)
      
      try:
        exec(match['code'], module)
      except ImportPermissionError as err:
        if err.name in ["socket", "requests",]:
          await ctx.reply(f"**Para proteger a privacidade de quem está me ospedando, é impossível importar a lib `{err.name}` pois com ela da para descobrir a sua localização.**")

          return
      except:
        await ctx.reply(f"```{traceback.format_exc()}```")
      
      main = module.get('main')

      if not main:
        return

      try:
        await main(ctx)
      except:
        await ctx.reply(f"```{traceback.format_exc()}```")

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Commands(bot))