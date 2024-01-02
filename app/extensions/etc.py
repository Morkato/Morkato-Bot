from discord.ext     import commands

from typing import (
  Optional,
  Literal,
  Callable,
  Coroutine,
  Any,
  Mapping,
  Sequence,
  Union,
  Tuple
)

import importlib.util
from types import ModuleType

import re

async def compile_python_code(code: str, ctx: commands.Context, globals: Optional[dict[str, Any]] = None) -> None:
  try:
    exec(compile(code, '<main>', 'exec'), globals)
  except Exception as err:
    await ctx.send(f'Error **`({type(err).__name__})`: {err}**')

    raise

  main_func = globals.get('main')
  
  if not main_func:
    return
  
  try:
    await main_func(ctx)
  except Exception as err:
    await ctx.send(f'Error **`({type(err).__name__})`: {err}**')

    raise
  
  await ctx.send('Compilado com sucesso!')

async def not_interpret_the_language(code: str, ctx: commands.Context, globals: Optional[dict[str, Any]] = None) -> None:
  await ctx.send('Eu não sei interpretar essa linguagem.')

def compile_code(type: str) -> Callable[[str, commands.Context, Optional[dict[str, Any]]], Coroutine[Any, Any, None]]:
  if type in [ 'py', 'python' ]:
    return compile_python_code
  
  return not_interpret_the_language

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

class Commands(commands.Cog):  
  @commands.command(name='console')
  async def console(self, ctx: commands.Context, /, *, code: str) -> None:
    if not ctx.isDev and not ctx.author.id in [ 510948690354110464, 963130404204867694, 600394147047800973 ]:
      await ctx.send('Esse comando é exclusivo para desenvolvedores.')

      return
    
    code_type, code = get_code(code)
    
    if not code_type and not code:
      await ctx.reply("**Não sei interpretar essa linguagem T-T**")

      return

    call = compile_code(code_type)

    await call(code, ctx, globalsModules)

async def setup(bot: commands.Bot) -> None:
  cog = Commands(bot)

  await bot.add_cog(cog)
