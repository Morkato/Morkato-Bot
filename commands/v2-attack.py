from typing import Union, Dict, List

from morkato.converters import CommandConverter
from .                  import utils

from morkato import (
  MorkatoBot,
  MorkatoContext,
  Cog
)

from discord.ext import commands

import re

class Attack(Cog, name='v2-Attack'):
  @commands.command(name='v2-a')
  async def attack(self, ctx: MorkatoContext, *, cmd: CommandConverter) -> None:
    guild = ctx.morkato_guild

    if not cmd.params:
      if not cmd.base:
        await ctx.send('Ok, mas qual o nome?')

        return
      
      attacks = guild.get_attacks_by_name(cmd.base)

      attack = attacks[0]

      await ctx.send_attack(attack)

      return

async def setup(bot: MorkatoBot) -> None:
  await bot.add_cog(Attack(bot))