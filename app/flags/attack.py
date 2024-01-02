from __future__ import annotations

from typing import (
  TYPE_CHECKING,
  ClassVar,
  Union,
  List
)

if TYPE_CHECKING:
  from morkato.context import MorkatoContext

  from app.utils.flags import (
    BaseType,
    FlagDataType
  )

from morkato.utils.etc import message_checker, reaction_checker, in_range, fmt
from morkato.art       import Art
from app.utils.flags   import (
  FlagGroup,
  flag
)

__all__ = ('AttackFlagGroup',)

class AttackFlagGroup(FlagGroup):
  CREATE_MESSAGE_IF_NAME_IS_NONE: ClassVar[str] = "Beleza, beleza, vamos criar um ataque... Um ataque sem nome?"
  CREATE_MESSAGE_IF_NAME_ART_IS_NONE: ClassVar[str] = "Okok, você quer que eu crie um ataque sem uma arte? Tá correto isso aí?"
  CREATE_MESSAGE_ATTACK_HAS_CREATED: ClassVar[str] = "Um novo ataque chamado: **`{attack.name}`** foi criado."

  RENAME_MESSAGE_NAME_IS_NONE: ClassVar[str] = "Tranquilo, irei renomear o ataque chamado... Chamado... Chamado, pera, cadê?"
  RENAME_MESSAGE_RENAME_IS_NONE: ClassVar[str] = "Tranquilo, irei renomear o ataque chamado: **`{NAME}`** para... Para... Pera, vou renomear, para que?"
  RENAME_MESSAGE_IF_ATTACK_HAS_EDITED: ClassVar[str] = "O ataque chamado: **`{before}`** foi renomeado para: **`{after}`**."

  @flag(aliases=['c'])
  async def create(self, ctx: MorkatoContext, art_name: BaseType, names: FlagDataType) -> None:
    cls = self.__class__

    if art_name is None:
      await ctx.send(cls.CREATE_MESSAGE_IF_NAME_ART_IS_NONE)

      return
    
    if not names:
      await ctx.send(cls.CREATE_MESSAGE_IF_NAME_IS_NONE)

      return
    
    art = ctx.morkato_guild.get_art(art_name)
    attack = await art.create_attack(name=names[0])

    await ctx.send(cls.CREATE_MESSAGE_ATTACK_HAS_CREATED.format(attack=attack))
  
  @flag(aliases=['r'])
  async def rename(self, ctx: MorkatoContext, name: BaseType, names: FlagDataType) -> None:
    cls = self.__class__
    
    if name is None:
      await ctx.send(cls.RENAME_MESSAGE_NAME_IS_NONE)

      return
    
    if not names:
      await ctx.send(cls.RENAME_MESSAGE_RENAME_IS_NONE)

      return
  
    attack = ctx.morkato_guild.get_attack(name)

    before = attack.name
    after = names[0]

    attack = await attack.edit(name=after)

    await ctx.send(cls.RENAME_MESSAGE_IF_ATTACK_HAS_EDITED.format(before=before, after=after))