from typing import Callable, Coroutine, Union, Any

from utils.string import Context, format_variables as format

from utils.guild  import Guild

async def format_text(ctx: Context, guild: Guild, /) -> None:
  text = ctx.get_param('name')
  
  variables = guild.vars

  kwargs = { v.name: v.text for v in variables }

  text = format(text, **kwargs)

  await ctx.send(text)

flags = {
  'DEFAULT': format_text
}

def get(flag: str) -> Union[Callable[[Context, Guild], Coroutine[Any, Any, None]], None]:
  return flags.get(flag)