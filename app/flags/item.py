from __future__ import annotations

from typing import (
  TYPE_CHECKING,
  ClassVar,
  Union,
  List
)

if TYPE_CHECKING:
  from morkato.types._etc import Context
  from morkato.player import Player

  from app.utils.flags import (
    BaseType,
    FlagDataType
  )

from morkato.utils.etc import message_checker, reaction_checker, in_range, fmt
from morkato.errors    import ErrorType, NotFoundError
from morkato.item      import PlayerItem
from discord.embeds    import Embed
from discord.user      import User
from morkato.art       import Art
from app.utils.flags   import (
  FlagGroup,
  flag
)

__all__ = ('AttackFlagGroup',)

class ItemGroupFlag(FlagGroup):
  CTX_LIMIT_ITEMS_PAGE: ClassVar[int] = 10

  USE_MESSAGE_IF_NAME_IS_NONE: ClassVar[str] = "Como irei saber o item sem um nome?"
  USE_MESSAGE_IF_ITEM_IS_NOT_USABLE: ClassVar[str] = "O item {item.name} não é usável."

  @staticmethod
  def create_embed_inventory(usr: User, player: Player, items: List[PlayerItem]) -> Embed:
    embed = Embed()

    embed.set_author(
      name=player.name,
      icon_url=player._appearance or usr.display_avatar._url
    )

    embed.set_footer(text='ID: %s' % player.id, icon_url=usr.display_avatar._url)

    for item in items:
      embed.add_field(
        name='%s: %s' % (item.item_name, item._amount),
        value=item.item._description or "No description",
        inline=False
      )

    return embed
  
  @classmethod
  def create_embeds_inventory(cls, usr: User, player: Player) -> List[Embed]:
    inventory = player.inventory
    items = (inventory[chunk:chunk+cls.CTX_LIMIT_ITEMS_PAGE] for chunk in range(0, len(inventory), cls.CTX_LIMIT_ITEMS_PAGE))

    embeds = [ cls.create_embed_inventory(usr, player, chunk) for chunk in items]

    return embeds
  
  @flag(aliases=['u'])
  async def use(self, ctx: Context, name: BaseType, names: FlagDataType) -> None:
    cls = self.__class__
    
    if names:
      name = names[0]

    if name is None:
      await ctx.send(cls.USE_MESSAGE_IF_NAME_IS_NONE)
      
      return
    
    item = ctx.morkato_guild.get_item(name)
    
    if not item._usable:
      await ctx.send(cls.USE_MESSAGE_IF_ITEM_IS_NOT_USABLE.format(item=item))

      return
    
    raise NotImplementedError
  
  @flag(aliases=['i'])
  async def inventory(self, ctx: Context, name: BaseType, names: FlagDataType) -> None:
    cls = self.__class__
    player = None
    
    try:
      player = ctx.player
    except NotFoundError as error:
      if not error.type == ErrorType.PLAYER_NOTFOUND:
        raise error from None
      raise error

    embeds = self.create_embeds_inventory(ctx.author, player)

    await ctx.send_page_embed(embeds)