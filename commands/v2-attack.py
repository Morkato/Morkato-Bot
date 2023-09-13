from .v2.attack import AttackGroupFlags

from morkato.converters import CommandConverter
from morkato            import (
  MorkatoContext,
  MorkatoBot,
  Cog,
  
  utils
)

from discord.ext import commands

class Attack(Cog, name='v2-Attack'):
  GROUP = AttackGroupFlags()

  @commands.command(name='v2-a', cls=utils.LoggerCommand)
  async def attack(self, ctx: MorkatoContext, *, cmd: CommandConverter) -> None:
    guild = ctx.morkato_guild

    print(cmd.params)
    
    if not cmd.params:
      if not cmd.base:
        await ctx.send('Ok, mas qual o nome?')

        return
      
      attacks = guild.get_attacks_by_name(cmd.base)

      attack = attacks[0]

      await ctx.send_attack(attack)

      return
    
    await utils.process_flags(Attack.GROUP, ctx=ctx, base=cmd.base, params=cmd.params)

async def setup(bot: MorkatoBot) -> None:
  await bot.add_cog(Attack(bot))