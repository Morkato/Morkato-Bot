from utils.commands import message_page_embeds
from utils import Guild, getGuild
from discord.ext import commands

import discord

async def respiration(guild: Guild) -> list[discord.Embed]:
  respirations = guild.get_arts('RESPIRATION')
  
  embeds = [ discord.Embed(title='Respirações', description='\n'.join(f'**{index} - *`{resp.name}`***' for index, resp in enumerate(respirations[i:i+10], start=i+1))) for i in range(0, len(respirations), 10) ]

  return embeds

class List(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
  
  @commands.command(name='list')
  async def List(self, ctx: commands.Context, /, *, name: str) -> None:
    guild = getGuild(ctx.guild)

    if name == 'respiration':
      embeds = await respiration(guild)

    
    await message_page_embeds(ctx, self.bot, embeds)

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(List(bot))