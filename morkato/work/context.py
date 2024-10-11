from __future__ import annotations
from .utility import (SelectMenuEmbed, SelectMenuView, ConfirmationView)
from .embeds import (EmbedBuilder, EmbedBuilderView)
from discord.ext.commands.context import Context
from .types import (SelectMenuObject, ArrayType)
from morkato.errors import MorkatoException
from typing import (
  TYPE_CHECKING,
  Optional,
  Callable,
  TypeVar,
  Dict,
  Any
)
if TYPE_CHECKING:
  from discord import (Message, Embed)  
  from .bot import MorkatoBot
else:
  MorkatoBot = Any
  Message = Any
  Embed = Any

SelectMenuObjectT = TypeVar('SelectMenuObjectT', bound=SelectMenuObject)

class ConfirmationFailure(MorkatoException): ...

class MorkatoContext(Context[MorkatoBot]):
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
  async def send_select_menu(
    self, models: ArrayType[SelectMenuObjectT], *,
    title: Optional[str] = None,
    description: str,
    line_style: str,
    selected_line_style: str,
    key: Callable[[SelectMenuObjectT], EmbedBuilder]
  ) -> SelectMenuObjectT:
    builder = SelectMenuEmbed(
      models = models,
      title = title,
      description = description,
      line_style = line_style,
      selected_line_style = selected_line_style
    )
    view = SelectMenuView(builder, self.bot.loop, key)
    embed = await builder.build(0)
    message = await self.send(embed=embed, view=view)
    model = await view.get()
    await message.edit(view=None)
    return model
  async def send_confirmation(self, *args, **kwargs) -> Message:
    view = ConfirmationView(self.bot.loop)
    kwargs["view"] = view
    message = await self.send(*args, **kwargs)
    result = await view.get()
    if not result:
      raise ConfirmationFailure
    return message