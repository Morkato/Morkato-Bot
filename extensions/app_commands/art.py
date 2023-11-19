"""
  Morkato BOT Extension: "ART";

    - com.morkato.bot.commands.app_commands.art;

      - /artedit ~ [Moderação] Edita uma arte já existente;
"""

from typing import Optional

from .views.embeds import Embeds

from discord import app_commands
from morkato import (
  MorkatoBot,
  Cog,

  utils,
  errors
)

import discord

choices_types_arts = [
  app_commands.Choice(name='Respirações', value='RESPIRATION'),
  app_commands.Choice(name='Kekkijutsus', value='KEKKIJUTSU'),
  app_commands.Choice(name='Estilos de Luta', value='FIGHTING_STYLE')
]

choices_types_art = [
  app_commands.Choice(name='Respiração', value='RESPIRATION'),
  app_commands.Choice(name='Kekkijutsu', value='KEKKIJUTSU'),
  app_commands.Choice(name='Estilo de Luta', value='FIGHTING_STYLE')
]

class ArtAppCommands(Cog):
  @app_commands.command(
    name='art',
    description='[RPG] Exibe uma arte determinando pelo nome'
  )
  @app_commands.rename(name='art')
  async def art(self, interaction: discord.Interaction, name: str) -> None:
    if not interaction.guild:
      await interaction.response.send_message('Esse comando é exclusivo para servidores :/')

      return

    await interaction.response.defer()

    player = None
    
    try:
      player = self.get_player(interaction.user)
    except errors.NotFoundError: ...
    
    art    = self.get_art(interaction.guild, name)
    embeds = [ (emd.set_author(
      name=player.name if player else "Anonymous",
      icon_url=player.appearance or interaction.user.display_avatar.url if player else interaction.user.display_avatar.url
    )) for emd in art.embed_at() ]

    idx = 0
    
    if len(embeds) == 1:
      await interaction.edit_original_response(embed=embeds[idx])

      return
    
    await interaction.edit_original_response(embed=embeds[idx], view=Embeds(embeds, start=idx))

  @app_commands.command(
    name='arts',
    description='[RPG] Mostra todas as artes presente em um servidor.'
  )
  @app_commands.choices(map_by=choices_types_arts)
  @app_commands.rename(map_by='map')
  async def art_list(self, interaction: discord.Interaction, map_by: Optional[app_commands.Choice[str]]) -> None:
    if not interaction.guild:
      await interaction.response.send_message('Esse comando é exclusivo para servidores :/')

      return
    
    await interaction.response.defer()

    guild = self.get_guild(interaction.guild)
    arts  = (art for art in guild.arts if not art.excluded)

    embeds = list(utils.organize_arts(arts, map_by.value) if map_by else utils.organize_arts(list(arts)))
    
    idx = 0

    if len(embeds) == 1:
      await interaction.edit_original_response(embed=embeds[idx])

      return
    
    view = Embeds(embeds, start=idx)

    await interaction.edit_original_response(embed=embeds[idx], view=view)

  @app_commands.command(
    name='artedit',
    description='[Moderação] Edita uma arte.'
  )
  @app_commands.rename(art_name='art', banner_uri='banner-url')
  @app_commands.choices(type=choices_types_art)
  async def art_edit(self, interaction: discord.Interaction, art_name: str,
    name:        Optional[str],
    type:        Optional[app_commands.Choice[str]],
    title:       Optional[str],
    description: Optional[str],
    banner:      Optional[discord.Attachment],
    banner_uri:  Optional[str]
  ) -> None:
    if not interaction.guild:
      await interaction.response.send_message('Esse comando é exclusivo para servidores :/')

      return
    
    if not interaction.user.guild_permissions.manage_guild:
      await interaction.response.send_message('Você não tem permissão para executar esse comando.')

      return
    
    await interaction.response.defer()
    
    guild = self.get_guild(interaction.guild)

    payload = {  }

    if name:
      name = utils.strip_text(name, strip_text=True, ignore_empty=True, empty=' ')

      if not utils.in_range(len(name), (2, 32)):
        await interaction.edit_original_response(content='Um nome deve ter no mínimo 2 à 32 caracteres.')

        return
      
      payload['name'] = name
  
    if type:
      payload['type'] = type.value
    
    if title:
      title = utils.strip_text(title, strip_text=True, ignore_empty=True, empty=' ')

      if not utils.in_range(len(title), (1, 96)):
        await interaction.edit_original_response(content='Um título deve ter no mínimo 1 à 92 caracteres.')

        return
      
      payload['title'] = title
    
    if description:
      description = utils.strip_text(description, strip_text=True)

      if not utils.in_range(len(description), (1, 4096)):
        await interaction.edit_original_response(content='Uma descrição deve ter no mínimo 1 à 4092 caracteres.')

        return
      
      payload['description'] = description
    
    if banner:
      if not banner.content_type.startswith('image/'):
        await interaction.edit_original_response(content='Apenas imagens ou GIF no banner beleza?')

        return
      
      payload['url'] = utils.strip_text(banner.url, strip_text=True)
    
    if not payload:
      await interaction.edit_original_response(content='Pera, pera, deixa eu ver o que você editou... Pera quê?')
      
      return

    art = guild.get_art(art_name)

    art_name = art.name
    art_type = art.type

    art = await art.edit(**payload)

    if art_type == 'RESPIRATION':
      await interaction.edit_original_response(content=f'A respiração: **`{art_name}`** foi editada.')

    elif art_type == 'KEKKIJUTSU':
      await interaction.edit_original_response(content=f'O kekkijutsu: **`{art_name}`** foi editado.')
    
    elif art_type == 'FIGHTING_STYLE':
      await interaction.edit_original_response(content=f'O estilo de luta: **`{art_name}`** foi editado.')

async def setup(bot: MorkatoBot) -> None:
  await bot.add_cog(ArtAppCommands(bot))
