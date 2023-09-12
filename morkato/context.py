from __future__ import annotations

from typing import (
  TYPE_CHECKING,
  List
)

from discord.ext.commands import Context

if TYPE_CHECKING:
  from .client import MorkatoBot

  from .objects.player import Player
  from .objects.attack import Attack
  from .objects.art    import Art
  

  import discord

class MorkatoContext(Context['MorkatoBot']):
  @property
  def player(self) -> Player:
    return self.bot.database.get_player(guild_id=str(self.guild.id), id=str(self.author.id))
  
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
        reaction, user = await self.bot.wait_for('reaction_add', timeout=20, check= lambda reaction, user: user.id == self.author.id and self.guild.id == reaction.message.guild.id and self.channel.id == reaction.message.channel.id and message.id == reaction.message.id)
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
  
  async def send_art(self, art: Art) -> discord.Message:
    embeds = None
    
    try:
      player = self.player
      embeds = [ embed.set_author(name = player.name, icon_url = player.appearance or self.author.display_avatar.url) for embed in await art.embed_at()]
    
    except:
      embeds = await art.embed_at()

    return await self.send_page_embed(embeds)
  
  async def send_attack(self, attack: Attack) -> discord.Message:
    embed = None

    try:
      player = self.player
      embed = (await attack.embed_at()).set_author(name = player.name, icon_url = player.appearance or self.author.display_avatar.url)
    except:
      embed = await attack.embed_at()

    await self.send(embed=embed)