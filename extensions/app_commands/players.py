from typing import Optional

from .views.players import breed

from discord import app_commands
from morkato import (
  MorkatoBot,
  Cog,

  errors
)

import requests
import discord

MAX_CONTENT_LENGTH = 8 * 1024 * 1024

class AppCommandsPlayers(Cog):
  @app_commands.command(
    name="pme",
    description="[RPG] Mostra o jogador de um usuário."
  )
  async def player_status(self, interaction: discord.Interaction, usr: Optional[discord.Member]) -> None:
    if not interaction.guild:
      await interaction.response.send_message("Esse comando está disponível apenas em servidores.")
      
      return
    
    usr = usr or interaction.user
    
    if usr.bot:
      await interaction.response.send_message("Bot nem é jogador :/")
      
      return
    
    guild = self.bot.get_morkato_guild(interaction.guild)
    
    try:
      player = guild.get_player(usr)

      await interaction.response.send_message(embed=player.embed)
    except errors.NotFoundError:
      if usr.id == interaction.user.id:
        await interaction.response.send_message("Você não possui registro.")

        return
      
      await interaction.response.send_message(f"Não achei o registro do: **`@{usr.name}`** :V")
  
  @app_commands.command(
    name="pregister",
    description="[Moderação] Registra um novo jogador."
  )
  @app_commands.choices(breed=breed)
  async def player_register(self,
    interaction:   discord.Interaction,
    usr:           discord.Member,
    name:          str,
    breed:         app_commands.Choice[str],
    appearance:    Optional[discord.Attachment],
    appearanceurl: Optional[str],
    life:          Optional[int],
    breath:        Optional[int],
    blood:         Optional[int],
    force:         Optional[int],
    resistance:    Optional[int],
    velocity:      Optional[int],
    credibility:   Optional[int],
    cash:          Optional[int],
    exp:           Optional[int]
  ) -> None:
    if not interaction.guild:
      await interaction.response.send_message("Esse comando está disponível apenas em servidores.")
      
      return
    
    guild = None
    
    try:
      guild = self.database.get_guild(interaction.guild)
    except errors.NotFoundError:
      await interaction.response.send_message("Esse servidor precisa ser configurado.")

      return
    
    if not interaction.user.guild_permissions.manage_guild:
      await interaction.response.send_message("Você precisa da permissão de gerenciar o servidor para executar esse comando.")
      
      return
    
    usr = usr or interaction.user
    
    if usr.bot:
      await interaction.response.send_message("Bot nem é jogador :/")
      
      return
    
    try:
      player = self.database.get_player(usr)

      await interaction.response.send_message(f"O **`@{usr.name}`** já está registrado.")

      return
    except errors.NotFoundError: pass

    optional = {  }
    
    if appearance:
      if not appearance.content_type.startswith("image/"):
        await interaction.response.send_message("Por favor, uma imagem.")

        return
      
      optional['appearance'] = appearance.url
    
    if appearanceurl:
      res = requests.get(appearanceurl, stream=True)
      headers = res.headers

      if not headers.get('content-type') or not headers['content-type'].startswith('image/'):
        await interaction.response.send_message("A URL da aparência do usuário é invalida.")

        return

      if not headers.get('content-length') or headers['content-length'] > MAX_CONTENT_LENGTH:
        await interaction.response.send_message("Favor, aceito apenas imagens de até 8MB")

        return
      
      optional["appearance"] = appearanceurl

    if life:
      optional['life'] = life

    if breath:
      optional['breath'] = breath
    
    if blood:
      optional['blood'] = blood
    
    if force:
      optional['force'] = force

    if resistance:
      optional['resistance'] = resistance
    
    if velocity:
      optional['velocity'] = velocity
    
    if credibility:
      optional['credibility'] = credibility

    if cash:
      optional['cash'] = cash

    if exp:
      optional['exp'] = exp

    await interaction.response.defer()

    player = await guild.create_player(id=usr.id, name=name, breed=breed.value, **optional)

    await interaction.edit_original_response(content=f"Foi registrado o player: **`{player.name}`** em nome do: **`@{usr.name}`**")
  
  @app_commands.command(
    name="pedit",
    description="[Moderação] Edita um jogador já existente."
  )
  @app_commands.choices(breed=breed)
  async def player_edit(self,
    interaction:   discord.Interaction,
    usr:           Optional[discord.Member],
    name:          Optional[str],
    breed:         Optional[app_commands.Choice[str]],
    appearance:    Optional[discord.Attachment],
    appearanceurl: Optional[str],
    life:          Optional[int],
    breath:        Optional[int],
    blood:         Optional[int],
    force:         Optional[int],
    resistance:    Optional[int],
    velocity:      Optional[int],
    credibility:   Optional[int],
    cash:          Optional[int],
    exp:           Optional[int]
  ) -> None:
    if not interaction.guild:
      await interaction.response.send_message("Esse comando está disponível apenas em servidores.")
      
      return
    
    usr = usr or interaction.user
    
    if not interaction.user.guild_permissions.manage_guild or not usr.id == interaction.user.id:
      await interaction.response.send_message("Você precisa da permissão de gerenciar o servidor para executar esse comando em outros jogadores.")
      
      return
    
    if usr.bot:
      await interaction.response.send_message("Bot nem é jogador :/")
      
      return
    
    player = None

    try:
      player = self.database.get_player(usr)
    except errors.NotFoundError:
      if usr.id == interaction.user.id:
        await interaction.response.send_message("Você não possui registro.")

        return
      
      await interaction.response.send_message(f"Não achei o registro do: **`@{usr.name}`** :V")
    
    optional = {  }

    if name:
      optional['name'] = name

    if breed:
      optional['breed'] = breed.value
    
    if appearance:
      if not appearance.content_type.startswith("image/"):
        await interaction.response.send_message("Por favor, uma imagem.")

        return
      
      optional['appearance'] = appearance.url
    
    if appearanceurl:
      res = requests.get(appearanceurl, stream=True)
      headers = res.headers

      if not headers.get('content-type') or not headers['content-type'].startswith('image/'):
        await interaction.response.send_message("A URL da aparência do usuário é invalida.")

        return

      if not headers.get('content-length') or headers['content-length'] > MAX_CONTENT_LENGTH:
        await interaction.response.send_message("Favor, aceito apenas imagens de até 8MB")

        return
      
      optional["appearance"] = appearanceurl

    if life:
      optional['life'] = life

    if breath:
      optional['breath'] = breath
    
    if blood:
      optional['blood'] = blood
    
    if force:
      optional['force'] = force

    if resistance:
      optional['resistance'] = resistance
    
    if velocity:
      optional['velocity'] = velocity
    
    if credibility:
      optional['credibility'] = credibility

    if cash:
      optional['cash'] = cash

    if exp:
      optional['exp'] = exp

    if not optional:
      await interaction.response.send_message("Minha impressão, ou você não editou nada?")
      
      return

    await interaction.response.defer()
    player = await player.edit(**optional)

    await interaction.edit_original_response(content=f"Tudo certo, editei o player do usuário: **`@{usr.name}`**")

async def setup(bot: MorkatoBot) -> None:
  await bot.add_cog(AppCommandsPlayers(bot))