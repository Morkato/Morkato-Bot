from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from morkato.types._etc import Context
  from morkato.bot import MorkatoBot

from app.converters.flags      import FlagConverter, FlagDataType
from app.flags.art             import ArtFlagGroup
from discord.ext.commands.core import command
from discord.ext.commands.cog  import Cog

class Group(ArtFlagGroup): ...

class ArtCog(Cog):
  GROUP: Group

  @command(aliases=['arte'])
  async def art(self, ctx: Context, *, chunk: FlagDataType = FlagConverter) -> None:
    (name, flags) = chunk

    if flags:
      result = await self.GROUP.invoke(ctx, name, flags)

      if not result:
        await ctx.send("Essa flag não existe.")
      
      return

    if name is None:
      await ctx.send("Bem, vou procurar, vamos ver... Procurar o nada? Como assim?")

      return

    art = ctx.morkato_guild.get_art(name)

    await ctx.send_page_embed(ctx.charge_player_embeds(art.embeds))

async def setup(bot: MorkatoBot) -> None:
  ArtCog.GROUP = Group()

  cog = ArtCog(bot)

  await bot.add_cog(cog)