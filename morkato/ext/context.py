from __future__ import annotations
from .embeds import (EmbedBuilder, EmbedBuilderView)
from discord.ext.commands.context import Context
from typing import (
  TYPE_CHECKING,
  Optional,
  Dict,
  Any
)
if TYPE_CHECKING:
  from discord import (Message, Embed)
  from morkato.guild import Guild
  from .bot import MorkatoBot
else:
  MorkatoBot = Any
  Message = Any
  Guild = Any
  Embed = Any
class MorkatoContext(Context[MorkatoBot]):
  morkato_guild: Optional[Guild] = None
  async def send_embed(self, builder: EmbedBuilder, *, resolve_all: bool = False, wait: bool = True) -> Message:
    cache: Dict[int, Embed] = {}
    length = builder.length()
    if length == 0:
      raise NotImplementedError
    embed = await builder.build(0)
    message = await self.send(embed=embed)
    if length == 1:
      return message
    cache[0] = embed
    if resolve_all and length != -1:
      cache |= {
        idx: await builder.build(idx)
        for idx in range(1, length)
      }
    view = EmbedBuilderView(
      builder=builder,
      length=length,
      cache=cache
    )
    await message.edit(view=view)
    if wait:
      await view.wait()
    return message