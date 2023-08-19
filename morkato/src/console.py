from typing import (
  Optional,
  Coroutine,
  Callable,
  Literal,

  Any
)

from discord.ext import commands

CodeType = Literal['python', 'py']

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

def compile_code(type: CodeType) -> Callable[[str, commands.Context, Optional[dict[str, Any]]], Coroutine[Any, Any, None]]:
  if type in [ 'py', 'python' ]:
    return compile_python_code
  
  return not_interpret_the_language