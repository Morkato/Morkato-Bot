from app.interfaces import RolledObjectModel
from discord.embeds import Embed
from typing import (Dict, List)
from .base import BaseEmbedBuilder

class EmbedBuilderRolledObject(BaseEmbedBuilder):
  def __init__(
    self, models: List[RolledObjectModel], *,
    rolled: Dict[int, int],
    quantity: int,
    title: str,
    style: str
    ) -> None:
    self.description = self.builder.safe_get_content(self.LANGUAGE, "rolledObjectDescription", quantity=quantity)
    self.quantity = quantity
    self.models = models
    self.rolled = rolled
    self.style = style
    self.title = title
  async def build_base_embed(self) -> Embed:
    return Embed(
      title = self.title,
      description = self.description
    )
  async def build(self, page: int) -> Embed:
    embed = await self.build_base_embed()
    description = embed.description
    description += '\n\n'
    start_chunk = page * self.CHUNK_SIZE
    try:
      for i in range(start_chunk, start_chunk + self.CHUNK_SIZE):
        obj = self.models[i]
        description += self.style.format(i + 1, obj.percent, obj.name, self.rolled.get(obj.id, 0))
        description += '\n'
    except IndexError:
      pass
    embed.description = description
    return embed
  def length(self) -> int:
    length = len(self.models)
    if length == 0:
      return 1
    elif length % self.CHUNK_SIZE != 0:
      return length // self.CHUNK_SIZE + 1
    return length // self.CHUNK_SIZE
class FamilyRolledBuilder(EmbedBuilderRolledObject):
  def __init__(
    self, models: List[RolledObjectModel], *,
    rolled: Dict[int, int],
    quantity: int
  ) -> None:
    super().__init__(
      models = models,
      rolled = rolled,
      quantity = quantity,
      title = self.builder.safe_get_content_unknown_formatting(self.LANGUAGE, "rolledFamiliesTitle"),
      style = self.builder.safe_get_content_unknown_formatting(self.LANGUAGE, "rolledFamiliesLineStyle")
    )
class AbilityRolledBuilder(EmbedBuilderRolledObject):
  def __init__(
    self, models: List[RolledObjectModel], *,
    rolled: Dict[int, int],
    quantity: int
  ) -> None:
    super().__init__(
      models = models,
      rolled = rolled,
      quantity = quantity,
      title = self.builder.safe_get_content_unknown_formatting(self.LANGUAGE, "rolledAbilitiesTitle"),
      style = self.builder.safe_get_content_unknown_formatting(self.LANGUAGE, "rolledAbilitiesLineStyle")
    )