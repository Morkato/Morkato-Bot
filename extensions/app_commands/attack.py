from typing import Optional

from discord import app_commands, ui

from morkato import (
  MorkatoBot,
  Cog,

  utils
)

import discord

MESSAGE_I_FLAG = """$name = $n    = {name!r}
$damage = $d  = {damage}
$breath = $br = {breath}
$blood = $bl  = {blood}
$title = $t   = {title}
"""

class AppCommandAttack(Cog):
  @app_commands.command(
    name='ainfo',
    description='[RPG] Ataca com um ataque do RPG.'
  )
  async def attack(self, interaction: discord.Interaction, name: str) -> None:
    ...
    
  @app_commands.command(
    name='acreate',
    description="[Moderação] Cria um novo ataque."
  )
  @app_commands.rename(art_name='art', arm_name='arm', parent_name='parent')
  async def attack_create(self, interaction: discord.Interaction,
    arm_name:    Optional[str],
    parent_name: Optional[str],
    art_name:    Optional[str],
    name:        str,
    title:       Optional[str],
    description: Optional[str],
    image:       Optional[discord.Attachment],
    imageurl:    Optional[str],
    damage:      Optional[int],
    breath:      Optional[int],
    blood:       Optional[int]
  ) -> None:
    if not interaction.guild:
      await interaction.response.send_message('Esse comando está disponível em servidores apenas.')
      
      return
    
    if not interaction.user.guild_permissions.manage_guild:
      await interaction.response.send_message('Você não tem permissão para editar um ataque.')

      return

    await interaction.response.defer()

    guild = self.get_guild(interaction.guild)
    
    name = utils.strip_text(name, ignore_empty=True, strip_text=True, empty=' ')

    if not utils.in_range(len(name), (2, 32)):
      await interaction.edit_original_response(content='O nome de um ataque deve ter no mínimo entre 2 à 32 caracteres.')

      return

    payload = { 'name': name }

    if len([item for item in [arm_name, parent_name, art_name] if item]) != 1:
      await interaction.edit_original_response(content='Você tem que passar uma art, arm ou parent, só pode ser um dos três.')

      return
    
    if art_name:
      payload['art'] = guild.get_art(art_name)

    if arm_name:
      payload['arm'] = guild.get_arm(arm_name)
    
    if parent_name:
      payload['parent'] = guild.get_attack(parent_name)
    
    if image:
      if not image.content_type.startswith('image/'):
        await interaction.edit_original_response(content='O arquivo precisa ser uma imagem ou GIF.')
        
        return
      
      payload['url'] = image.url

    if imageurl:
      payload['url'] = imageurl

    if title is not None:
      title = utils.strip_text(title, ignore_empty=True, strip_text=True, empty=' ')

      if not utils.in_range(len(title), (1, 96)):
        await interaction.edit_original_response(content='O título de um ataque deve ter no mínimo entre 1 à 92 caracteres.')

        return
      
      payload['embed_title'] = title
    
    if description is not None:
      description = utils.strip_text(description, strip_text=True)

      if not utils.in_range(len(description), (1, 4096)):
        await interaction.edit_original_response(content='O description de um ataque deve ter no mínimo entre 1 à 4092 caracteres.')

        return
      
      payload['embed_description'] = description
    
    if damage is not None:
      if not utils.in_range(damage, (0, utils.UINT_LIMIT)):
        await interaction.edit_original_response(content=f'Parece meio estanho, mas o dano não pode ser menor que 0 e maior que {utils.UINT_LIMIT}')

        return

      payload['damage'] = damage
    
    if breath is not None:
      if not utils.in_range(breath, (0, utils.UINT_LIMIT)):
        await interaction.edit_original_response(content=f'Parece meio estanho, mas o fôlego não pode ser menor que 0 e maior que {utils.UINT_LIMIT}')

        return

      payload['breath'] = breath
    
    if blood is not None:
      if not utils.in_range(blood, (0, utils.UINT_LIMIT)):
        await interaction.edit_original_response(content=f'Parece meio estanho, mas o sangue não pode ser menor que 0 e maior que {utils.UINT_LIMIT}')

        return

      payload['blood'] = blood
    
    if not payload:
      await interaction.edit_original_response(content='Eu tô ficando doido oou você não editou nada?')

      return
    
    attack = await guild._attacks.create(**payload)

    await interaction.edit_original_response(content=f'Um ataque chamado: **`{attack}`** foi criado.')

  @app_commands.command(
    name='aedit',
    description="[Moderação] Edita atributos de um ataque."
  )
  @app_commands.rename(attack_name='attack')
  async def attack_edit(self, interaction: discord.Interaction, attack_name: str,
    name:        Optional[str],
    title:       Optional[str],
    description: Optional[str],
    image:       Optional[discord.Attachment],
    imageurl:    Optional[str],
    damage:      Optional[int],
    breath:      Optional[int],
    blood:       Optional[int]
  ) -> None:
    if not interaction.guild:
      await interaction.response.send_message('Esse comando está disponível em servidores apenas.')
      
      return
    
    if not interaction.user.guild_permissions.manage_guild:
      await interaction.response.send_message('Você não tem permissão para editar um ataque.')

      return

    await interaction.response.defer()
    
    guild = self.get_guild(interaction.guild)

    fmt = lambda text: utils.strip_text(text,
      ignore_accents=True,
      ignore_empty=True,
      case_insensitive=True,
      strip_text=True
    )

    attack_name = fmt(attack_name)

    
    attack = utils.get(guild._attacks, lambda attack: fmt(attack.name) == attack_name)

    if not attack:
      await interaction.edit_original_response(content='Esse ataque não existe.')

      return
    
    payload = {  }

    if name:
      name = utils.strip_text(name, ignore_empty=True, strip_text=True, empty=' ')

      if not utils.in_range(len(name), (2, 32)):
        await interaction.edit_original_response(content='O nome de um ataque deve ter no mínimo entre 2 à 32 caracteres.')

        return
      
      payload['name'] = name
    
    if image:
      if not image.content_type.startswith('image/'):
        await interaction.edit_original_response(content='O arquivo precisa ser uma imagem ou GIF.')
        
        return
      
      payload['url'] = image.url

    if imageurl:
      payload['url'] = imageurl
    
    if title is not None:
      title = utils.strip_text(title, ignore_empty=True, strip_text=True, empty=' ')

      if not utils.in_range(len(title), (1, 96)):
        await interaction.edit_original_response(content='O título de um ataque deve ter no mínimo entre 1 à 92 caracteres.')

        return
      
      payload['title'] = title
    
    if description is not None:
      description = utils.strip_text(description, strip_text=True)

      if not utils.in_range(len(description), (1, 4096)):
        await interaction.edit_original_response(content='O description de um ataque deve ter no mínimo entre 1 à 4092 caracteres.')

        return
      
      payload['description'] = description
    
    if damage is not None:
      if not utils.in_range(damage, (0, utils.UINT_LIMIT)):
        await interaction.edit_original_response(content=f'Parece meio estanho, mas o dano não pode ser menor que 0 e maior que {utils.UINT_LIMIT}')

        return

      payload['damage'] = damage
    
    if breath is not None:
      if not utils.in_range(breath, (0, utils.UINT_LIMIT)):
        await interaction.edit_original_response(content=f'Parece meio estanho, mas o fôlego não pode ser menor que 0 e maior que {utils.UINT_LIMIT}')

        return

      payload['breath'] = breath
    
    if blood:
      if not utils.in_range(blood, (0, utils.UINT_LIMIT)):
        await interaction.edit_original_response(content=f'Parece meio estanho, mas o sangue não pode ser menor que 0 e maior que {utils.UINT_LIMIT}')

        return

      payload['blood'] = blood
    
    if not payload is not None:
      await interaction.edit_original_response(content='Eu tô ficando doido oou você não editou nada?')

      return
    
    await attack.edit(**payload)

    await interaction.edit_original_response(content=f'O ataque chamado: **`{attack.name}`** foi editado.')

async def setup(bot: MorkatoBot) -> None:
  await bot.add_cog(AppCommandAttack(bot))
