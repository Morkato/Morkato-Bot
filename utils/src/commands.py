from __future__ import annotations

from typing import (
  Optional,
  Callable,
  Coroutine,
  Union,
  
  TYPE_CHECKING,
  Dict,
  Any
)

from discord.ext     import commands
from objects.guild   import Guild
from parsers.command import parse

import discord
import inspect

if TYPE_CHECKING:
  from morkato.client import Morkato

CommandFunction = Callable[[commands.Context, Guild, Union[str, None], Union[str, None], Dict[str, str]], Coroutine[Any, Any, None]]

async def make_event(
  event:    CommandFunction,
  ctx:      commands.Context,
  guild:    Guild,
  value:    Optional[Union[str, None]] = None,
  value_in: Optional[Union[str, None]] = None,
  params:   Optional[Dict[str, str]]   = None
) -> None:
  signatured = inspect.signature(event)

  parameters = signatured.parameters

  length = len(parameters)

  if length < 2:
    raise Exception(f'Internal error in event `{event.__name__}`')
  
  required_params = [ctx, guild]
  optional_params = [value, value_in, params]

  length_params = length - 2
  
  event_params = required_params + optional_params[:length_params]

  await event(*event_params)


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

async def command_by_flag(
  *, flag_gether: Callable[[str], Union[CommandFunction, None]],
  ctx: commands.Context,
  db: Morkato,
  text: str
) -> None:
  for task in text.split('&'):
    flag, value, value_in, params = parse(task)

    event = flag_gether(flag or 'DEFAULT')

    if not event:
      await ctx.send('Que flag é essa?')

      return
    
    if not event.__doc__:
      return await make_event(
        event,
        ctx,
        db.guilds.get(str(ctx.guild.id)),
        value,
        value_in,
        params
      )

    permission = getattr(ctx.author.guild_permissions, event.__doc__)

    if permission is None:
      await ctx.send('Erro de permissões.')

      return

    if not permission:
      await ctx.send('Você não tem permissão para executar essa flag.')

      return

    await make_event(
      event,
      ctx,
      db.guilds.get(str(ctx.guild.id)),
      value,
      value_in,
      params
    )