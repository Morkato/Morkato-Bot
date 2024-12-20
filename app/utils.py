from morkato.abc import UnresolvedSnowflakeList
from .interfaces import ObjectWithPercentT
from .errors import ModelsEmptyError
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
  if len(models) == 0:
    raise ModelsEmptyError()
  objs = [elem for elem in models if filter(elem)] if filter is not None else models
  if len(objs) == 0:
    raise ModelsEmptyError()
  total = sum(obj.percent for obj in objs)
  generated = randint(0, total)
  current = 0
  for obj in objs:
    current += obj.percent
    is_valid = 0 >= generated - current
    if is_valid:
      break
  return obj