from discord.ext     import commands

from  .groups.commands import TestingGroupFlag

from morkato.converters import CommandConverter
from morkato import MorkatoContext, Cog, compile_code, utils

from typing import (
  Mapping,
  Sequence,
  Union,
  Tuple
)

import importlib.util
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
  if not text.startswith('```') and not text.endswith('```'):
    return None, None

  if not '\n' in text:
    return None, None
    
  text = text[3:]
  
  code_type, code = text.split('\n', 1)

  return code_type, code[:-3]

globalsModules = {
  "__builtins__": {
    "__import__": __load__,
    "sum": sum,
    'sorted': sorted,
    'hash': hash,
    "max": max,
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
  GROUP: TestingGroupFlag

  @commands.command(name='console')
  async def console(self, ctx: commands.Context, /, *, code: str) -> None:
    if not ctx.author.id in [ 510948690354110464, 963130404204867694, 600394147047800973 ]:
      return
    
    code_type, code = get_code(code)
    
    if not code_type and not code:
      await ctx.reply("**Não sei interpretar essa linguagem T-T**")

      return

    call = compile_code(code_type)

    await call(code, ctx, globalsModules)
  
  @commands.command()
  async def developer(self, ctx: MorkatoContext, /, *, cmd: CommandConverter) -> None:
    if cmd.params:
      await utils.process_flags(self.GROUP, ctx=ctx, base=cmd.base, params=cmd.params)
  
  @commands.command(name='dev-items')
  async def dev_items(self, ctx: MorkatoContext, module: str) -> str:
    module, cls_name = '.'.join(module.split('.')[:-2]), module.split('.')[-1]

    spec = importlib.util.find_spec(module)

    if not spec:
      return
    
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    cls = getattr(module, cls_name, None)

    if not cls:
      return
    
    items = getattr(cls, 'ITEMS', None)

    if not isinstance(items, set):
      return
    
    print(cls_name)
    
    length = len(items)
    content = ''

    iterable = iter(items)
    
    content += '<'
    if length >= 1:
      content += '\n  ' + str(next(iterable)) + '\n'
    
    if length >= 2:
      content += '  ' + str(next(iterable)) + '\n'
    
    if length >= 3:
      content += '  ' + str(next(iterable)) + '\n'
    
    if length >= 4:
      content += f'[...] More items ({cls.__name__}): ' + str(length - 3) + '\n'
    
    content += '>'

    del iterable

    await ctx.send(f'``` {content} ```')

async def setup(bot: commands.Bot) -> None:
  cog = Commands(bot)

  Commands.GROUP = TestingGroupFlag(cog)

  await bot.add_cog(cog)
