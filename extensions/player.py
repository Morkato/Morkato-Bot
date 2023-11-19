from typing import Optional

from .groups.player import PlayerGroupFlag

from morkato.converters import CommandConverter, Context
from morkato import (
  MorkatoContext,
  MorkatoBot,
  
  Cog,

  utils,
  errors
)

from discord.ext import commands

class Player(Cog):
  EMPTY_CONTEXT = Context()
  GROUP: PlayerGroupFlag

  def __init__(self, bot: MorkatoBot) -> None:
    super().__init__(bot)

  @commands.command(name='me', aliases=['status'])
  async def v2me(self, ctx: MorkatoContext, *, cmd: Optional[CommandConverter]) -> None:
    cmd = cmd or self.EMPTY_CONTEXT

    if cmd.params:
      await utils.process_flags(self.GROUP, ctx=ctx, base=cmd.base, params=cmd.params)

      return
    
    member = ctx.author
      
    if cmd.base:
      member = await commands.MemberConverter().convert(ctx, cmd.base)
        
    try:
      player = ctx.morkato_guild.get_player(member)

      await ctx.send_player(player)

      return
        
    except errors.NotFoundError: pass

    if member.id == ctx.author.id:
      await ctx.send('Você não possui registro.')

      return
          
    await ctx.send('Pera, essa pessoa não tem registro :/')

async def setup(bot: commands.Bot) -> None:
  cog = Player(bot)

  Player.GROUP = PlayerGroupFlag(cog)

  await bot.add_cog(cog)
