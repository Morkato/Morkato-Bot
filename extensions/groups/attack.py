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

MESSAGE_I_FLAG = """```
$name = $n    = {name!r}
$damage = $d  = {damage}
$breath = $br = {breath}
$blood = $bl  = {blood}
$title = $t   = {title!r}
```"""

class AttackGroupFlags(utils.FlagGroup):
  @utils.flag(name='create', aliases=[ 'c' ])
  async def create(self, ctx: MorkatoContext, base: BaseType, param: ParamType) -> None:
    if not param:
      await ctx.send('Beleza tô criando e..... Cadê o nome?!')
      
      return
    
    art = utils.UNDEFINED

    guild = ctx.morkato_guild

    if base:
      art = guild.get_art(base)

    attack = await guild._attacks.create(name=param[0], art=art)

    ctx.debug_counter()

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

    attack = ctx.morkato_guild.get_attack(name)

    ctx.debug_counter()

    embed = attack.embed_at()

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
        
      
      embed = attack.embed_at(
        title=payload.get('title'),
        description=payload.get('description'),
        url=payload.get('url')
      )

      original_message = await original_message.edit(embed=embed)

  @utils.flag(name='delete', aliases=[ 'd' ])
  async def delete(self, ctx: MorkatoContext, base: BaseType, param: ParamType) -> None:
    if not ctx.author.guild_permissions.manage_guild:
      await ctx.send("Você não tem permissão para apagar um ataque.")

      ctx.debug_counter()

      return
    
    if not base and not param:
      await ctx.send('Ok, mas qual é o nome?')

      ctx.debug_counter()

      return
    
    name = param[0] if param else base

    attack = self.cog.get_attack(ctx.guild, name)

    art_type = None
    parent   = None
    
    if attack.art:
      art_type = attack.art.type
    
    elif attack.parent:
      parent = attack.parent

    ctx.debug_counter()
    
    content = f'Tem certeza que deseja deletar o ataque com o nome: **`{attack.name}`**'
    
    if art_type:
      if art_type == 'RESPIRATION':
        content = f'Tem certeza que deseja deletar o ataque com o nome: **`{attack.name}`** da respiração: **`{attack.art.name}`**'

      elif art_type == 'KEKKIJUTSU':
        content = f'Tem certeza que deseja deletar o ataque com o nome: **`{attack.name}`** do kekkijutsu: **`{attack.art.name}`**'

      elif art_type == 'FIGHTING_STYLE':
        content = f'Tem certeza que deseja deletar o ataque com o nome: **`{attack.name}`** do estilo de luta: **`{attack.art.name}`**'
    
    elif parent:
      content = f'Tem certeza que deseja deletar o ataque com o nome: **`{attack.name}`** derivada de: **`{parent.name}`**'

    msg = await ctx.send(content=content)

    await msg.add_reaction('✅')
    await msg.add_reaction('❌')

    (reaction, usr) = await self.cog.bot.wait_for('reaction_add', timeout=20, check=utils.reaction_checker(ctx, msg, [ 'author', 'channel', 'guild', 'message' ]))

    if str(reaction.emoji) == '✅':
      attack = await attack.delete()

      await ctx.send(f'O ataque: **`{attack.name}`** foi excluído.')

      return
    
    elif str(reaction.emoji) == '❌':
      await ctx.send('Ainda bem que tem a confirmação né não?')

  @utils.flag(name='info', aliases=[ 'i' ])
  async def info(self, ctx: MorkatoContext, base: BaseType, param: ParamType) -> None:
    if not base and not param:
      await ctx.send('Ok, mas qual é o nome?')

      ctx.debug_counter()

      return
    
    name = param[0] if param else base

    attack = self.cog.get_attack(ctx.guild, name)

    ctx.debug_counter()

    await ctx.send(MESSAGE_I_FLAG.format(name=attack.name, damage=attack.damage, breath=attack.breath, blood=attack.blood, title=attack.title))

  @utils.flag(name='rename', aliases=[ 'r' ])
  async def rename(self, ctx: MorkatoContext, base: BaseType, param: ParamType) -> None: ...
  @utils.flag(name='list', aliases=[ 'l' ])
  async def list(self, ctx: MorkatoContext, base: BaseType, param: ParamType) -> None: ...
    