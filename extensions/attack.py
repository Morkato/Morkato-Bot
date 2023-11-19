from .groups.attack import AttackGroupFlags

from morkato.converters import CommandConverter
from morkato            import (
  MorkatoContext,
  MorkatoBot,
  Cog,
  
  utils
)

from discord.ext import commands

class Attack(Cog):
  GROUP: AttackGroupFlags

  @staticmethod
  def _is_arm_attack(text: str) -> bool:
    return ':' in text

  async def _process_attack(self, ctx: MorkatoContext, name: str) -> None:
    attack = self.get_attack(ctx.guild, name)

    ctx.debug_counter()

    await ctx.send_attack(attack)
  
  async def _process_attack_arm(self, ctx: MorkatoContext, *, arm_name: str, attack_name: str) -> None:
    arm_name, attack_name = utils.strip_text(arm_name, strip_text=True, ignore_empty=True), utils.strip_text(attack_name, strip_text=True, ignore_empty=True)

    if utils.is_empty_text(arm_name) or utils.is_empty_text(attack_name):
      return
    
    arm = ctx.morkato_guild.get_item(arm_name)
    attack = arm.get_attack(attack_name)

    await ctx.send_attack(attack)
  
  @commands.command(name='a')
  async def attack(self, ctx: MorkatoContext, *, cmd: CommandConverter) -> None:
    ctx.debug_counter()
    
    if cmd.params:
      await utils.process_flags(Attack.GROUP, ctx=ctx, base=cmd.base, params=cmd.params)

      return
    
    if not cmd.base:
      await ctx.send('Ok, mas qual o nome?')

      return
      
    if not self._is_arm_attack(cmd.base):
      return await self._process_attack(ctx, cmd.base)
    
    arm_name, attack_name = cmd.base.split(':', 1)

    await self._process_attack_arm(ctx, arm_name=arm_name, attack_name=attack_name)
    
async def setup(bot: MorkatoBot) -> None:
  cog = Attack(bot)

  Attack.GROUP = AttackGroupFlags(cog)

  await bot.add_cog(cog)
