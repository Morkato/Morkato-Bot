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
  async def Edit_Art(self, ctx: commands.Context, /, name: str, *, json: str) -> None:
    guild = getGuild(ctx.guild)

    art = guild.get_art(name)

    if art is None:
      await ctx.send('Essa arte não existe.')

      return
    
    data = loads(json)

    art = art.edit(**data)

    await ctx.send('Editada')
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Art(bot))