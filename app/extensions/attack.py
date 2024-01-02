from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from morkato.context import MorkatoContext
  from morkato.bot import MorkatoBot

from app.converters.flags      import FlagConverter, FlagDataType
from app.flags.attack          import AttackFlagGroup
from discord.ext.commands.core import command
from discord.ext.commands.cog  import Cog

class Group(AttackFlagGroup): ...

class AttackCog(Cog):
  GROUP: Group

  @command(aliases=['a', 'ataque'])
  async def attack(self, ctx: MorkatoContext, *, chunk: FlagDataType = FlagConverter) -> None:
    (name, flags) = chunk

    if flags:
      result = await self.GROUP.invoke(ctx, name, flags)

      if not result:
        await ctx.send("Essa flag não existe.")
      
      return

    if name is None:
      await ctx.send("Bem, vou procurar, vamos ver... Procurar o nada? Como assim?")

      return

    attack = ctx.morkato_guild.get_attack(name)
    embed = ctx.charge_player_embed(attack.embed)

    await ctx.send(embed=embed)

async def setup(bot: MorkatoBot) -> None:
  AttackCog.GROUP = Group()

  cog = AttackCog(bot)

  await bot.add_cog(cog)