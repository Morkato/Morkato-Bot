from discord.ext     import commands
from parsers.command import parse

from morkato import Cog, compile_code

from typing import (
  Mapping,
  Sequence,
  Union,
  Tuple
)

from types import ModuleType

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

def get_code(text: str) -> Tuple[Union[str, None], Union[str, None]]:
  code = re.match(r"```(?P<type>[A-Za-z0-9]+)\n(?P<code>[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ0-9.,\(\)/\"\'\\\\|\^\:;!@#\$%&`\*\=\+\-\<\>~\[\]\{\}$?_\s]+)```", text, re.IGNORECASE)

  if code is None:
    return None, None

  code_type = code['type']
  code      = re.sub(r'\\`', '`', code['code'])

  return code_type, code

globalsModules = {
  "__builtins__": {
    "__import__": __load__,
    'object': object,
    'range': range,
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
    "__name__": '<main>',
    "property": property,
    "super": super,
    "type": type,
    "map": map,
    "next": next,
    "print": print,
    'round': round,
    'len': len
  }
}

class Commands(Cog):
  @commands.command(name='console')
  async def Console(self, ctx: commands.Context, /, *, code: str) -> None:
    if not ctx.author.id in [ 510948690354110464, 963130404204867694 ]:
      return
    
    code_type, code = get_code(code)
    
    if not code_type and not code:
      await ctx.reply("**Não sei interpretar essa linguagem T-T**")

      return

    call = compile_code(code_type)

    await call(code, ctx, globalsModules)
  
  @commands.command(name='parse')
  async def Parse(self, ctx: commands.Context, /, *, text: str) -> None:
    await ctx.send(f'**`{parse(text)}`**')

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Commands(bot))