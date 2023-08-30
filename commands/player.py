from typing import Optional

from .ext import command_by_flag

from morkato.client import MorkatoBot, Cog
from discord.ext    import commands

from .flags.player import PlayerCommand

import discord

class Player(Cog):
  def __init__(self, bot: MorkatoBot) -> None:
    super().__init__(bot)

    self.player_command = PlayerCommand()

  @commands.command(name='me')
  async def me(self, ctx: commands.Context, member: Optional[discord.Member], *, text: Optional[str] = None) -> None:
    if not member:
      member = ctx.author

    await command_by_flag(command=self.player_command, ctx=ctx, util=member, db=self.db, text=text or '')

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Player(bot))