from typing import Optional

from .groups.item import ItemGroupFlag

from morkato.converters import CommandConverter
from morkato import (
  MorkatoContext,
  MorkatoBot,
  
  Cog,

  utils
)

from discord.ext import commands

class Item(Cog):
  GROUP: ItemGroupFlag

  @commands.command(aliases=['i'])
  async def item(self, ctx: MorkatoContext, *, cmd: CommandConverter) -> None:
    if cmd.params:
      await utils.process_flags(self.GROUP, ctx=ctx, base=cmd.base, params=cmd.params)

      return
    
async def setup(bot: MorkatoBot) -> None:
  cog = Item(bot)

  Item.GROUP = ItemGroupFlag(cog)

  await bot.add_cog(cog)