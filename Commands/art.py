from typing import Optional

from utils.commands import message_page_embeds
from discord import app_commands
from discord.ext import commands
from utils.string import toKey
from utils import getGuild

import discord

class Art(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
  @commands.command(aliases=['Arte'])
  async def Art(self, ctx: commands.Context, /, *, art_name: str) -> None:
    guild = getGuild(ctx.guild)

    art = guild.get_art(art_name)
    
    if art is None:
      await ctx.send('Essa arte não existe.')

      return
    
    await ctx.send(f'**`{art.attacks}`**')

    await message_page_embeds(ctx, self.bot, art.embeds)

  @commands.command(name='del-art')
  async def Delete_Art(self, ctx: commands.Context, /, *, name: str) -> None:
    guild = getGuild(ctx.guild)

    art = guild.del_art(name)

    await ctx.send(f'A arte chamada **`{art.name}`** foi deletada.')
  @commands.command(name='attacks')
  async def Attack(self, ctx: commands.Context, /) -> None:
    guild = getGuild(ctx.guild)

    await ctx.send(f'`{guild.attacks}`')
  
  @commands.command(name='new-resp')
  async def New_Respiration(self, ctx: commands.Context, /, *, name: str) -> None:
    guild = getGuild(ctx.guild)

    resp = guild.new_respiration(name)

    await ctx.send(f'Uma nova respiração chamada: **`{resp.name}`** foi criada!')

  @commands.command(name='new-kekki')
  async def New_Kekkijutsu(self, ctx: commands.Context, /, *, name: str) -> None:
    guild = getGuild(ctx.guild)

    kekki = guild.new_kekkijutsu(name)

    await ctx.send(f'Um novo kekkijutsu chamado **`{kekki.name}`** foi criado!')
  
  @commands.command(name='edit-art')
  async def Edit_Art(self, ctx: commands.Context, /, *, name: str) -> None:
    guild = getGuild(ctx.guild)

    art = guild.get_art(name)

    if art is None:
      await ctx.send('Essa arte não existe.')

      return
    
    await ctx.send(f'started event... Breaking in : 1min')

    payload = {}

    embed_message = await ctx.send(embed=next(iter(art.embed_at())))

    while True:
      message = await self.bot.wait_for('message', timeout=300, check=lambda message: message.author.id == ctx.author.id and message.channel.id == ctx.channel.id and message.guild.id == ctx.guild.id)

      content = message.content.strip()

      key, value = (content[:content.find('!')], content[content.find('!')+1:]) if not content.find('!') == -1 else (None, content)

      if key is None and value.lower() == 'done':
        if not payload:
          await ctx.send('A arte abordada foi editada.')

          return
        
        art.edit(**payload)

        await ctx.send('A arte abordada foi editada.')

        return

      elif key == 'title':
        payload['embed_title'] = value

        await message.add_reaction('✅')

      elif key == 'description':
        payload['embed_description'] = value

        await message.add_reaction('✅')

      elif key == 'url':
        payload['embed_url'] = value

        await message.add_reaction('✅')

      await message.delete()

      embed_message = await embed_message.edit(embed=next(iter(art.embed_at(title=payload.get('embed_title'), description=payload.get('embed_description'), url=payload.get('embed_url')))))
  
  @commands.command(aliases=['a'])
  async def Attack(self, ctx: commands.Context, /, *, name: str) -> None:
    guild = getGuild(ctx.guild)

    attack = guild.get_attack(name)

    if not attack:
      await ctx.send('Esse ataque não existe.')

      return

    await ctx.send(embed=attack.embed_at(ctx.author))

  @app_commands.command(name='a')
  async def slash_Attack(self, interaction: discord.Interaction, name: str) -> None:
    guild = getGuild(interaction.guild)

    attack = guild.get_attack(name)

    if not attack:
      await interaction.response.send_message('Esse ataque não existe.', silent=True)

      return
    
    await interaction.response.send_message(embed=attack.embed_at(member=interaction.user))
  @commands.command(name='new-attack')
  async def New_Attack(self, ctx: commands.Context, /, art_name: str, *, name: str) -> None:
    guild = getGuild(ctx.guild)

    art = guild.get_art(art_name)

    if art is None:
      await ctx.send('Essa arte não existe.')

      return
    
    attack = art.new_attack(name)

    await ctx.send(f'Uma novo ataque chamado **`{attack}`** foi criado.')
  
  @commands.command(name='del-attack')
  async def Del_Attack(self, ctx: commands.Context, /, name: str) -> None:
    guild = getGuild(ctx.guild)

    attack = guild.get_attack(name)

    if attack is None:
      await ctx.send('Esse ataque não existe.')

      return
    
    attack = attack.delete()

    await ctx.send(f'O ataque com o nome **`{attack}`** foi deletado.')
  
  @commands.command(name='edit-attack')
  async def Edit_Attack(self, ctx: commands.Context, /, *, name: str) -> None:
    guild = getGuild(ctx.guild)

    attack = guild.get_attack(name)

    if attack is None:
      await ctx.send('Esse ataque não existe.')

      return
    
    payload = {}

    original_message = await ctx.send(embed=attack.embed_at())
    
    while True:
      message = await self.bot.wait_for('message', timeout=300, check=lambda message: message.author.id == ctx.author.id and message.channel.id == ctx.channel.id and message.guild.id == ctx.guild.id)

      content = message.content.strip()

      key, value = (content[:content.find('!')], content[content.find('!')+1:]) if not content.find('!') == -1 else (None, content)

      if key is None and value.lower() == 'done':
        if not payload:
          await ctx.send('O ataque abordada foi editada.')

          return
        
        attack.edit(**payload)

        await ctx.send('O ataque abordada foi editada.')

        return

      elif key == 'title':
        payload['embed_title'] = value

        await message.add_reaction('✅')

      elif key == 'description':
        payload['embed_description'] = value

        await message.add_reaction('✅')

      elif key == 'url':
        payload['embed_url'] = value

        await message.add_reaction('✅')
      
      elif key == 'damage':
        try: payload['damage'] = int(value)
        except:
          await message.add_reaction('❌')

          continue

        await message.add_reaction('✅')

      elif key == 'stamina':
        try:
          payload['stamina'] = int(value)
        except:
          await message.add_reaction('❌')

          continue

        await message.add_reaction('✅')
      else: continue
    
      await message.delete()

      original_message = await original_message.edit(embed=attack.embed_at(
        title=payload.get('embed_title'),
        description=payload.get('embed_description'),
        url=payload.get('embed_url'),
        damage=payload.get('damage'),
        stamina=payload.get('stamina'))
      )
    
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Art(bot))
