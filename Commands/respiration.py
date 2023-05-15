from typing import Optional

from discord.ext import commands
from json import loads
from utils import getGuild

class Respiration(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
  
  @commands.command(aliases=['Resp'])
  async def respiration(self, ctx: commands.Context, /, *, resp_name: Optional[str] = None) -> None:
    guild = getGuild(ctx.guild)

    if resp_name:
      respiration = guild.get_respiration(resp_name)

      if respiration is None:
        await ctx.send('Essa resiração não existe.')

        return
      await ctx.send(embed=respiration.embed)
      
      return
  
  @commands.command(aliases=['new-resp', 'create-resp'])
  async def new_resp(self, ctx: commands.Context, name: str, /, *, json: Optional[str] = None) -> None:
    guild = getGuild(ctx.guild)
    
    data = { "name": name }
    if json is not None:
      data = { **loads(json), **data }
    
    try:
      respiration = guild.new_respiration(**data)

      await ctx.reply(f'Uma nova arte chamada: **`{respiration}`** foi criada.')
    except Exception as err:
      await ctx.reply(f'Uma nova arte com o nome: {name} já existe.')
    
  @commands.command(aliases=['edit-resp'])
  async def edit_respiration(self, ctx: commands.Context, /, *, name: str) -> None:
    guild = getGuild(ctx.guild)

    respiration = guild.get_respiration(name)

    if respiration is None:
      await ctx.send('Essa resiração não existe.')

      return

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Respiration(bot))