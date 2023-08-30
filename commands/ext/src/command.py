from __future__ import annotations

from typing_extensions import Self

from typing import (
  Optional,
  Callable,
  Coroutine,
  Union,
  
  TYPE_CHECKING,
  List,
  Dict,
  Any
)

from .flag import Flag

from discord.ext     import commands
from parsers.command import parse

import discord

if TYPE_CHECKING:
  from morkato.client import MorkatoBot

CommandFunc = Callable[[commands.Context, Callable[[Any, str], Coroutine[Any, Any, None]]], Coroutine[Any, Any, None]]

class CommandMeta(type):
  __flags__: List[Flag] = []
  
  def __new__(cls, name: str, bases: Any, attrs: Dict[str, Any], **kwargs) -> Self:
    flags = []

    for key, obj in attrs.items():
      if not isinstance(obj, Flag) or key.startswith('__'):
        continue
      
      flags.append(obj)
    
    attrs['__flags__'] = flags
    
    return super().__new__(cls, name, bases, attrs, **kwargs)

class Command(metaclass=CommandMeta):
  def __init__(self, *, case_insensitive: Optional[bool] = False) -> None:
    self.case_insensitive = case_insensitive or False

async def message_page_embeds(ctx: commands.Context, bot: commands.Bot, embeds: list[discord.Embed]) -> None:
  message = await ctx.send(embed=embeds[0])

  length = len(embeds)

  if length == 1:
    return
  
  index = 0

  await message.add_reaction('⏪')
  await message.add_reaction('⏩')

  while True:
    try:
      reaction, user = await bot.wait_for('reaction_add', timeout=20, check= lambda reaction, user: user.id == ctx.author.id and ctx.guild.id == reaction.message.guild.id and ctx.channel.id == reaction.message.channel.id and message.id == reaction.message.id)
    except:
      await message.clear_reactions()

      return
    
    if str(reaction.emoji) == '⏪':
      index = length - 1 if index == 0 else index - 1

      await message.remove_reaction('⏪', user)
    elif str(reaction.emoji) == '⏩':
      index = 0 if index + 1 == length else index + 1

      await message.remove_reaction('⏩', user)

    await message.edit(embed=embeds[index])

async def command_by_flag(*,
  command: Command,
  ctx:     commands.Context,
  util:    Optional[Any] = None,
  client:  MorkatoBot,
  text:    str
) -> None:
  for task in text.split('&'):
    flag, value, value_in, params = parse(task)

    cls = command.__class__

    flag = flag or 'default'
    flag = flag if not command.case_insensitive else flag.lower()

    event = next((item for item in cls.__flags__ if flag in item.aliases), None)

    if not event:
      await ctx.send('Essa flag não existe')

      return

    guild = client.database.get_guild(str(ctx.guild.id))

    await event(command, ctx, guild, util, value, value_in, params)