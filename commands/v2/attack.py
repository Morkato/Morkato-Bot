from typing import (
  Union,

  List
)

from morkato import (
  MorkatoContext,
  utils
)

BaseType = Union[str, None]
ParamType = List[str]

class AttackGroupFlags(utils.FlagGroup):
  @utils.flag(name='create', aliases=[ 'c' ])
  async def create(self, ctx: MorkatoContext, base: BaseType, param: ParamType) -> None:
    if not param:
      await ctx.send('Beleza tô criando e..... Cadê o nome?!')
      
      return
    
    art = utils.UNDEFINED
    arm = utils.UNDEFINED

    guild = ctx.morkato_guild

    if base:
      art = guild.get_arts_by_name(base)[0]

    attack = await guild.create_attack(name=param[0], art=art)

    message = 'Um novo ataque com o nome: **`{0.name}`** foi criado'
    
    if not art:
      await ctx.send(message.format(attack))

      return
    
    if art.type == 'RESPIRATION':
      message = 'Um novo ataque com o nome: **`{0.name}`** foi criado na respiração: **`{1.name}`**'

    elif art.type == 'KEKKIJUTSU':
      message = 'Um novo ataque com o nome: **`{0.name}`** foi criado no kekkijutsu: **`{1.name}`**'
    
    elif art.type == 'FIGHTING_STYLE':
      message = 'Um novo ataque com o nome: **`{0.name}`** foi criado no estilo de luta: **`{1.name}`**'
    
    await ctx.send(message.format(attack, art))

  @utils.flag(name='edit', aliases=[ 'e' ])
  async def edit(self, ctx: MorkatoContext, base: BaseType, param: ParamType) -> None: ...
  @utils.flag(name='delete', aliases=[ 'd' ])
  async def delete(self, ctx: MorkatoContext, base: BaseType, param: ParamType) -> None: ...
  @utils.flag(name='rename', aliases=[ 'r' ])
  async def rename(self, ctx: MorkatoContext, base: BaseType, param: ParamType) -> None: ...
  @utils.flag(name='list', aliases=[ 'l' ])
  async def list(self, ctx: MorkatoContext, base: BaseType, param: ParamType) -> None: ...
    