from utils.commands import message_page_embeds
from utils import Guild, getGuild
from discord.ext import commands

import discord

async def respiration(guild: Guild) -> list[discord.Embed]:
  respirations = guild.get_arts('RESPIRATION')
  
  embeds = [ discord.Embed(
    title='Respirações',
    description='\n'.join(f'**{index} - *`{resp.name}`***' for index, resp in enumerate(
      respirations[i:i+10],
      start=i+1))
    ).set_image(
      url='https://i.pinimg.com/originals/a3/34/6c/a3346cc151cbb8c20c57d05e83c932f3.gif'
    ) for i in range(0, len(respirations), 10) ]

  return embeds

async def kekkijutsu(guild: Guild) -> list[discord.Embed]:
  kekkijutsus = guild.get_arts('KEKKIJUTSU')
  
  embeds = [ discord.Embed(
    title='Kekkijutsus',
    description='\n'.join(f'**{index} - *`{kekki.name}`***' for index, kekki in enumerate(
      kekkijutsus[i:i+10],
      start=i+1))
    ).set_image(
      url='https://img.quizur.com/f/img645a66819299d3.74304340.png?lastEdited=1683646088'
    ) for i in range(0, len(kekkijutsus), 10) ]

  return embeds

class List(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
  
  @commands.command(name='list')
  async def List(self, ctx: commands.Context, /, *, name: str) -> None:
    guild = getGuild(ctx.guild)

    if name.lower() == 'respiration':
      embeds = await respiration(guild)
    elif name.lower() == 'kekkijutsu':
      embeds = await kekkijutsu(guild)
    else:
      await ctx.send('Essa lista não existe.')
      
      return

    
    await message_page_embeds(ctx, self.bot, embeds)

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(List(bot))