from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from morkato.types._etc import Context
  from morkato.bot import MorkatoBot

from app.converters.flags      import FlagConverter, FlagDataType
from app.flags.item            import ItemGroupFlag
from discord.ext.commands.core import command
from discord.ext.commands.cog  import Cog

class Group(ItemGroupFlag): ...

class ItemCog(Cog):
  GROUP: Group

  @command(aliases=['i'])
  async def item(self, ctx: Context, *, chunk: FlagDataType = FlagConverter) -> None:
    guild = ctx.bot.get_morkato_guild(ctx.guild)

    (name, flags) = chunk

    if flags:
      await self.GROUP.invoke(ctx, name, flags)

      return

    if not name:
      await ctx.send('Pera, pera, qual o nome mesmo?')

      return
    
    item = guild.get_item(name)
    embeds = ctx.charge_player_embeds(item.embeds)

    await ctx.send_page_embed(embeds)

async def setup(bot: MorkatoBot) -> None:
  ItemCog.GROUP = Group()

  cog = ItemCog(bot)

  await bot.add_cog(cog)