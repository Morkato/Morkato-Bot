from morkato.ext.extension import (ApplicationExtension, extension, command)
from app.embeds import (AttackBuilder, ArtBuilder)
from morkato.ext.context import MorkatoContext
from morkato.attack import Attack
from typing import Annotated
from morkato.art import Art
from random import randint
from app.utils import (
  AttackConverter,
  ArtConverter
)

@extension
class RPGCommands(ApplicationExtension):
  @command(name="art")
  async def art(self, ctx: MorkatoContext, *, art: Annotated[Art, ArtConverter]) -> None:
    builder = ArtBuilder(art)
    await ctx.send_embed(builder, resolve_all=True)
  @command(name="attack", aliases=['a'])
  async def attack(self, ctx: MorkatoContext, *, attack: Annotated[Attack, AttackConverter]) -> None:
    builder = AttackBuilder(attack)
    await ctx.send_embed(builder, resolve_all=True)
  @command(name="ability")
  async def ability(self, ctx: MorkatoContext) -> None:
    if not ctx.morkato_guild.abilities.already_loaded():
      await ctx.morkato_guild.abilities.resolve()
    total = ctx.morkato_guild.abilities_percent
    generated = randint(0, total)
    filter_callback = lambda ability: True # Checks filter with context
    current = 0
    for ability in ctx.morkato_guild.abilities:
      if not filter_callback(ability):
        total -= ability.percent
        if generated > total:
          generated -= ability.percent
        continue
      current += ability.percent
      is_valid = 0 >= generated - current
      if is_valid:
        break
    await ctx.send("Você obteve: **`%s`**, com a chance: **`%s`** (Número sorteado: **`%s`** de **`%s`**)" % (ability.name, ability.percent, generated, total))