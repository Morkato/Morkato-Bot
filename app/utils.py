from morkato.abc import UnresolvedSnowflakeList
from morkato.guild import Guild
from morkato.user import User
from morkbmt.context import MorkatoContext
from .interfaces import ObjectWithPercentT
from .embeds import UserRegistryEmbed
from .errors import ModelsEmptyError
from .view import RegistryUserUi
from random import randint
from typing import (
  Callable,
  Optional
)

async def roll(
  models: UnresolvedSnowflakeList[ObjectWithPercentT], *,
  filter: Optional[Callable[[ObjectWithPercentT], bool]] = None
) -> ObjectWithPercentT:
  await models.resolve()
  objs = [elem for elem in models if filter(elem)] if filter is not None else models
  if len(objs) == 0:
    raise ModelsEmptyError()
  total = sum(obj.percent for obj in objs) - 1
  generated = randint(0, total)
  current = -1
  for obj in objs:
    current += obj.percent
    is_valid = 0 >= generated - current
    if is_valid:
      break
  return obj

async def send_user_registry(ctx: MorkatoContext, guild: Guild) -> Optional[User]:
  view = RegistryUserUi(guild, ctx.bot.loop)
  builder = UserRegistryEmbed(ctx.author)
  embed = builder.build(0)
  origin = await ctx.send(embed=embed, view=view)
  resp = await view.get()
  await origin.delete()
  return resp