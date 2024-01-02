from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

if TYPE_CHECKING:
  from discord.ext.commands.context import Context
  from morkato.bot import MorkatoBot

from discord.ext.commands.converter import MemberConverter, MemberNotFound
from app.converters.flags           import FlagConverter, FlagDataType
from discord.ext.commands.core      import command
from discord.ext.commands.cog       import Cog

class PlayerCog(Cog):
  member: ClassVar[MemberConverter] = MemberConverter()

  @command(aliases=['player', 'status', 'jogador'])
  async def me(self, ctx: Context[MorkatoBot], *, chunk: FlagDataType = FlagConverter) -> None:
    guild = ctx.bot.get_morkato_guild(ctx.guild)

    (name, _) = chunk

    usr = ctx.author
    
    if name:
      try:
        usr = await self.member.convert(ctx, name)
      except MemberNotFound:
        await ctx.send("Pera, pera, quem é esse aí?")

        return
    
    player = guild._get_player(usr)

    if not player:
      if ctx.author.id == usr.id:
        await ctx.send("Você não possui registro")

        return

      await ctx.send(f"O usuário: **`@{usr.name}`** não possui registro.")

      return
    
    await ctx.send(f'**`{player}`**')

async def setup(bot: MorkatoBot) -> None:
  cog = PlayerCog(bot)

  await bot.add_cog(cog)