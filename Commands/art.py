from typing import Optional

from discord.ext import commands
from utils import getGuild

from json import loads

class Art(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
  @commands.command(aliases=['Arte'])
  async def Art(self, ctx: commands.Context, /, *, art_name: Optional[str] = None) -> None:
    guild = getGuild(ctx.guild)

    if art_name:
      art = guild.get_art(art_name)

      if art is None:
        await ctx.send('Essa arte não existe.')

        return

      for embed in art.embeds:
        await ctx.send(embed=embed)
      
      return
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

      elif key == 'title':
        payload['embed_title'] = value

        await message.add_reaction('✅')

        continue
      elif key == 'description':
        payload['embed_description'] = value

        await message.add_reaction('✅')

        continue
      elif key == 'url':
        payload['embed_url'] = value

        await message.add_reaction('✅')

        continue
  
  @commands.command(name='new-attack')
  async def New_Attack(self, ctx: commands.Context, /, art_name: str, *, name: str) -> None:
    guild = getGuild(ctx.guild)

    art = guild.get_art(art_name)

    if art is None:
      await ctx.send('Essa arte não existe.')

      return
    
    attack = art.new_attack(name)

    await ctx.send(f'Uma novo ataque chamado **`{attack}`** foi criado.')
    
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Art(bot))