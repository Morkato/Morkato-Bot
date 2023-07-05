from .vars_utils import get as getVarFlag

from utils.commands import command_by_flag

from utils import getGuild

from discord.ext import commands

import discord

class Vars(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
  
  @commands.command(aliases=[ 'v', 'var' ])
  async def vars(self, ctx: commands.Context, /, *, text: str) -> None:
    await command_by_flag(flag_gether=getVarFlag, ctx=ctx, text=text)
  
  @commands.command(name='new-var')
  async def New_Var(self, ctx: commands.Context, /, name: str, roles: commands.Greedy[discord.Role]) -> None:
    guild = getGuild(ctx.guild)

    message = await self.bot.wait_for('message', timeout=300, check=lambda message: message.author.id == ctx.author.id and message.channel.id == ctx.channel.id and message.guild.id == ctx.guild.id)

    var = guild.new_var(name=name, text=message.content, roles=roles)

    await ctx.send(f'**{var}**')
  
  @commands.command(name='format-text')
  async def Format_Text(self, ctx: commands.Context, /, *, text) -> None:
    if text == '!$(exit())':
      await ctx.send('Agora não, valeu?')

      return
    
    guild = getGuild(ctx.guild)

    keys = { var.name: var.text for var in guild.vars }

    await ctx.send(format(text, **keys))

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Vars(bot))