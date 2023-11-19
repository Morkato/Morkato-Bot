from typing import Optional

from .views.users import MEMBERS_TYPE, member_choice

from discord import app_commands
from morkato import (
  MorkatoBot,
  Cog,

  utils
)

import discord

class AppCommandManagerUsers(Cog):
  @app_commands.command(
    name='urole-add',
    description="[Moderação] Adiciona um cargo para um usuário."
  )
  async def user_role_add(self, interaction: discord.Interaction, usr: discord.Member, role: discord.Role) -> None:
    if not interaction.guild:
      await interaction.response.send_message("Você precisa estar em um servidor.")

      return
    
    if role.position > interaction.guild.self_role.position and role.permissions.manage_roles:
      await interaction.response.send_message("Eu não consigo colocar cargo acima do meu em um membro.")

      return
    
    await interaction.response.defer(ephemeral=True)
    await usr.add_roles(role)

    await interaction.edit_original_response(content=f"Foi adicionado o cargo: **`@{role.name}`** para o membro: **`@{usr.name}`**.")
  
  @app_commands.command(
    name='usrole-add',
    description="[Moderação] Adiciona um cargo para todos os usuários em um servidor.",
  )
  @app_commands.choices(include=member_choice)
  async def users_role_add(self,
    interaction: discord.Interaction,
    role: discord.Role,
    include: Optional[app_commands.Choice[int]],
  ) -> None:
    if not interaction.guild:
      await interaction.response.send_message("Você precisa estar em um servidor.")

      return
    
    if role.position > interaction.guild.self_role.position and role.permissions.manage_roles:
      await interaction.response.send_message("Eu não consigo colocar cargo acima do meu em um membro.")

      return
      
    async with interaction.channel.typing():
      await interaction.response.defer()
    
      if include:
        include = include.value

      include = include or 3

      for usr in interaction.guild.members:
        if include != 3 and usr.bot and include == 1 or include != 3 and not usr.bot and include == 2:
          continue

        await usr.add_roles(role)

      await interaction.edit_original_response(content=f"Foi adicionado o cargo: **`@{role.name}`** para todos os membros presente nesse servidor.")
  
  @app_commands.command(
    name='urole-remove',
    description="[Moderação] Remove um cargo de um usuário."
  )
  async def user_role_remove(self, interaction: discord.Interaction, usr: discord.Member, role: discord.Role) -> None:
    if not interaction.guild:
      await interaction.response.send_message("Você precisa estar em um servidor.")

      return
    
    if role.position > interaction.guild.self_role.position and role.permissions.manage_roles:
      await interaction.response.send_message("Eu não consigo colocar cargo acima do meu em um membro.")

      return
    
    if not role in usr.roles:
      await interaction.response.send_message(f"Como eu vou remover o cargo do membro: **`@{usr.name}`** se ele não tem?")

      return
    
    await interaction.response.defer(ephemeral=True)
    await usr.remove_roles(role)

    await interaction.edit_original_response(content=f"Foi removido o cargo: **`@{role.name}`** para o membro: **`@{usr.name}`**.")

async def setup(bot: MorkatoBot) -> None:
  await bot.add_cog(AppCommandManagerUsers(bot))
