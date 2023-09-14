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
  async def edit(self, ctx: MorkatoContext, base: BaseType, param: ParamType) -> None:
    if not param and not base:
      await ctx.send('Ok, vamos editar a arte sem nome... Pera, ela não tem nome.')

      return
    
    name = base or param[0]

    attacks = ctx.morkato_guild.get_attacks_by_name(name)

    if len(attacks) > 1:
      await ctx.send('**`[!]`** Olha, essa arte tem mais de uma com o msm nome. Não ainda artes com o mesmo nome, mas... Aguarde, pelo menos consigo avisar.')

    attack = attacks[0]

    embed = await attack.embed_at()

    payload = {}

    original_message = await ctx.send(embed=embed)
    
    while True:
      message = await ctx.bot.wait_for('message', timeout=300, check=utils.message_checker(ctx, [ 'author', 'channel', 'guild' ]))

      prefix_index = message.content.find('!')

      prefix, content = (None, message.content) if prefix_index == -1 else (message.content[:prefix_index].lower(), message.content[prefix_index+1:])

      if prefix is None and content.lower() == 'done':
        if not payload:
          await ctx.send('Pera, pera... Ficando loco, ou você não editou nada?')

          return
        
        attack = await attack.edit(
          title=payload.get('title', utils.UNDEFINED),
          description=payload.get('description', utils.UNDEFINED),
          url=payload.get('url', utils.UNDEFINED)
        )

        await ctx.send(f'O ataque: **`{attack.name}`** foi editado.')
        
        return
      
      elif prefix is None and content.lower() == 'exit':
        return
      
      elif prefix == 'title':
        payload['title'] = content

        await message.delete()
      
      elif prefix in ['description', 'desc']:
        payload['description'] = content

        await message.delete()

      elif prefix == 'url':
        payload['url'] = content

        if message.attachments:
          attachment = message.attachments[0]

          payload['url'] = attachment.url
        
      
      embed = await attack.embed_at(
        title=payload.get('title'),
        description=payload.get('description'),
        url=payload.get('url')
      )

      original_message = await original_message.edit(embed=embed)

  @utils.flag(name='delete', aliases=[ 'd' ])
  async def delete(self, ctx: MorkatoContext, base: BaseType, param: ParamType) -> None: ...
  @utils.flag(name='rename', aliases=[ 'r' ])
  async def rename(self, ctx: MorkatoContext, base: BaseType, param: ParamType) -> None: ...
  @utils.flag(name='list', aliases=[ 'l' ])
  async def list(self, ctx: MorkatoContext, base: BaseType, param: ParamType) -> None: ...
    