from __future__ import annotations

from typing import (
  TYPE_CHECKING,
  List
)

from discord.ext.commands import Context

if TYPE_CHECKING:
  from .client import MorkatoBot

  from .player import Player
  from .attack import Attack
  from .guild  import Guild
  from .art    import Art

  import discord

from . import errors, utils

from functools import cached_property

import time

class MorkatoContext(Context['MorkatoBot']):
  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)

    self.counter = float('inf')

  @cached_property
  def player(self) -> Player:
    return self.morkato_guild.get_player(self.author)
  
  @cached_property
  def morkato_guild(self) -> Guild:
    return self.bot.get_morkato_guild(self.guild)
  
  def get_counter(self) -> float:
    return self.counter
  
  def debug_counter(self) -> None:
    if self.counter == float('inf'):
      self.counter = time.perf_counter()

      return
    
    self.counter = time.perf_counter() - self.counter

  async def send_page_embed(self, embeds: List[discord.Embed]) -> discord.Message:
    message = await self.send(embed=embeds[0])

    length = len(embeds)

    if length == 1:
      return
    
    index = 0

    await message.add_reaction('⏪')
    await message.add_reaction('⏩')

    while True:
      try:
        reaction, user = await self.bot.wait_for('reaction_add', timeout=20, check=utils.reaction_checker(self, message, [ 'author', 'channel', 'guild', 'message' ]))
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
  
  def get_player_embed(self, embed: discord.Embed) -> discord.Embed:
    try:
      player = self.player

      return embed.set_author(name = player.name, icon_url = player.appearance or self.author.display_avatar.url)
    except errors.NotFoundError:
      return embed.set_author(name = 'Anonymous')

  async def send_art(self, art: Art) -> discord.Message:    
    embeds = [ self.get_player_embed(embed) for embed in art.embed_at()]

    return await self.send_page_embed(embeds)
  
  async def send_attack(self, attack: Attack) -> discord.Message:
    embed = self.get_player_embed(attack.embed_at())

    await self.send(embed=embed)

  async def send_player(self, player: Player = utils.UNDEFINED) -> discord.Message:
    player = player or self.player

    return await self.send(embed=player.embed)