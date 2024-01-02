from __future__ import annotations

from typing import (
  TYPE_CHECKING,
  Generic,
  List
)

if TYPE_CHECKING:
  from .player import Player
  from .guild import Guild

  from discord.message import Message
  from discord.embeds import Embed

from discord.ext.commands.context import Context
from functools import cached_property

from .types._etc import MorkatoBotT, BotAppT
from .utils.etc import reaction_checker
from .errors import ErrorType, NotFoundError

class AppBotContext(Context[BotAppT], Generic[BotAppT]):
  @property
  def isDev(self) -> bool:
    if self.bot._dev is None or self.prefix is None:
      return False
    
    return self.bot._dev.match(self.prefix)

class MorkatoContext(AppBotContext[MorkatoBotT], Generic[MorkatoBotT]):
  @cached_property
  def player(self) -> Player:
    return self.morkato_guild.get_player(self.author)
  
  @cached_property
  def morkato_guild(self) -> Guild:
    return self.bot.get_morkato_guild(self.guild)
  
  async def send_page_embed(self, embeds: List[Embed]) -> Message:
    message = await self.send(embed=embeds[0])

    length = len(embeds)

    if length == 1:
      return
    
    index = 0

    await message.add_reaction('⏪')
    await message.add_reaction('⏩')

    while True:
      try:
        reaction, user = await self.bot.wait_for('reaction_add', timeout=20, check=reaction_checker(self, message, [ 'author', 'channel', 'guild', 'message' ]))
      except:
        await message.clear_reactions()

        return message
      
      if str(reaction.emoji) == '⏪':
        index = length - 1 if index == 0 else index - 1

        await message.remove_reaction('⏪', user)
      elif str(reaction.emoji) == '⏩':
        index = 0 if index + 1 == length else index + 1

        await message.remove_reaction('⏩', user)

      await message.edit(embed=embeds[index])
  
  def charge_player_embeds(self, embeds: List[Embed]) -> List[Embed]:
    return [ self.charge_player_embed(embed) for embed in embeds ]
  
  def charge_player_embed(self, embed: Embed) -> Embed:
    player_name = "anonymous"
    avatar = None

    try:
      player = self.player

      player_name = player._name
      avatar = player._appearance or self.author.display_avatar.url
    except NotFoundError as error:
      if not error.type == ErrorType.PLAYER_NOTFOUND:
        raise error from None

    embed.set_author(name=player_name, icon_url=avatar)

    return embed