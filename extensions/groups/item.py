from typing import (
  Union,

  List
)

from morkato import (
  MorkatoContext,
  Item,

  utils
)

import re

BaseType = Union[str, None]
ParamType = List[str]

class ItemGroupFlag(utils.FlagGroup):
  @staticmethod
  def _get_item(ctx: MorkatoContext, name_or_id: Union[str, int]) -> Item:
    guild = ctx.morkato_guild
    
    return guild.get_item(name_or_id)
  
  @utils.flag(aliases=[ 'i' ])
  async def info(self, ctx: MorkatoContext, base: BaseType, param: ParamType) -> None:
    if param:
      base = param[0]

    if not base:
      await ctx.send(f'Como sem um nome?')

      return
    
    item = self._get_item(ctx, base)

    await ctx.send(f'Info: **`{item}`**')
  
  @utils.flag(aliases=['u'])
  async def use(self, ctx: MorkatoContext, base: BaseType, param: ParamType) -> None:
    if param:
      base = param[0]

    if not base:
      await ctx.send(f'Como sem um nome?')

      return
    
    if re.match(r'^[0-9]+$', base):
      base = int(base)
    
    item = self._get_item(ctx, base)

    msg = 'Ainda em desenvolvimento., perdão :/' if item._usable else 'Ainda em desenvolvimento, mas posso adiantar pra você e falar que esse item não é utilizável.'

    await ctx.send(msg)
  
  @utils.flag(aliases=['r'])
  async def rename(self, ctx: MorkatoContext, base: BaseType, param: ParamType) -> None:
    if not base:
      await ctx.send(f'É necessário passar o nome, exemplo: ``` !item amoeba --{self.rename.name} new name```')

      return
    
    if not param:
      await ctx.send(f'É necessário especificar o nome pelo qual você quer trocar, exemplo: ``` !item amoeba --rename massinha```')

      return
    
    item = self._get_item(ctx, base)

    base = item.name

    item = await item.edit(name=param[0])

    await ctx.send(f'O item com o nome: **`{base}`** foi renomeado para: **`{item.name}`**.')
