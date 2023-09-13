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

class ArtGroupFlags(utils.FlagGroup):
  @utils.flag(name='create', aliases=[ 'c' ])
  async def create(self, ctx: MorkatoContext, base: BaseType, param: ParamType) -> None:
    if not base:
      await ctx.send('Tá bom, mas qual o tipo? Respiração, kekkijutsu, estilo de luta, qual?')

      return
    
    base = utils.extract_art_type(base)

    if not base:
      await ctx.send('Ok, mas que tipo de arte é esse?')

      return
    
    if not param:
      await ctx.send('Ok, irei criar quantas artes hoje?')

      return
    
    arts = [ await ctx.morkato_guild.create_art(name=name, type=base) for name in param ]

    message = 'Foi criada uma nova arte com o nome: **`{0.name}`**'

    if base == 'RESPIRATION':
      message = 'Foi criada uma nova respiração com o nome: **`{0.name}`**'

    elif base == 'KEKKIJUTSU':
      message = 'Foi criado um novo kekkijutsu com o nome: **`{0.name}`**'

    elif base == 'FIGHTING_STYLE':
      message = 'Foi criado um novo estilo de luta com o nome: **`{0.name}`**'

    await ctx.send('\n'.join(message.format(art) for art in arts))

  @utils.flag(name='edit', aliases=[ 'e' ])
  async def edit(self, ctx: MorkatoContext, base: BaseType, param: ParamType) -> None:
    if not param and not base:
      await ctx.send('Ok, vamos editar a arte sem nome... Pera, ela não tem nome.')

      return
    
    name = param[0] or base

    arts = ctx.morkato_guild.get_arts_by_name(name)

    if len(arts) > 1:
      await ctx.send('Olha, essa arte tem mais de uma com o msm nome. Não ainda artes com o mesmo nome, mas... Aguarde, pelo menos consigo avisar.')

    art = arts[0]

    embeds = await art.embed_at()
    embed = embeds[0]

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
        
        art = await art.edit(
          title=payload.get('title'),
          description=payload.get('description'),
          url=payload.get('url')
        )

        message = 'A arte: **`{0}`** foi editada.'

        if art.type == 'RESPIRATION':
          message = 'A respiração chamada: **`{0}`** foi editada.'

        elif art.type == 'KEKKIJUTSU':
          message = 'O kekkijutsu chamado: **`{0}`** foi editado.'

        await ctx.send(message.format(art))
        
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
        
      
      embeds = await art.embed_at(
        title=payload.get('title'),
        description=payload.get('description'),
        url=payload.get('url')
      )

      embed = embeds[0]

      original_message = await original_message.edit(embed=embed)

  @utils.flag(name='delete', aliases=[ 'd' ])
  async def delete(self, ctx: MorkatoContext, base: BaseType, param: ParamType) -> None:
    if not param and not base:
      await ctx.send('Ok, vamos editar a arte sem nome... Pera, ela não tem nome.')

      return
    
    name = param[0] or base

    arts = ctx.morkato_guild.get_arts_by_name(name)

    if len(arts) > 1:
      await ctx.send('Olha, essa arte tem mais de uma com o msm nome. Não ainda artes com o mesmo nome, mas... Aguarde, pelo menos consigo avisar.')

    art = arts[0]

    embeds = await art.embed_at()

    embed = embeds[0]
    
    message = await ctx.send('Tem certeza?', embed=embed)

    await message.add_reaction('✅')
    await message.add_reaction('❌')
    
    reaction, user = await ctx.bot.wait_for('reaction_add', timeout=20, check=utils.reaction_checker(ctx, message, [ 'author', 'guild', 'channel', 'message' ]))
    
    if str(reaction.emoji) == '✅':
      art = await art.delete()

      message = 'A arte com o nome: **`{0.name}`** foi deletada.'

      if art.type == 'RESPIRATION':
        message = 'A respiração chamada: **`{0.name}`** foi deletada.'

      elif art.type == 'KEKKIJUTSU':
        message = 'O kekkijutsu chamado: **`{0.name}`** foi deletado.'

      elif art.type == 'FIGHTING_STYLE':
        message = 'O estilo de luta chamado: **`{0.name}`** foi deletado.'
      
      await ctx.send(message.format(art))
    
    elif str(reaction.emoji) == '❌':
      await ctx.send('Ok, você mudou de ideia.')

  @utils.flag(name='rename', aliases=[ 'r' ])
  async def rename(self, ctx: MorkatoContext, base: BaseType, param: ParamType) -> None:
    if not base:
      await ctx.send('Bem, vamos trocar o nome do nada para... Hâ... Pera, como vou saber qual arte trocar sem o nome?!')

      return
    
    if not param:
      await ctx.send('Beleza, vamos editar o nome para nenhum nome?.. Tá certo isso??')
      
      return

    arts = ctx.morkato_guild.get_arts_by_name(base)

    if len(arts) > 1:
      await ctx.send('Olha, essa arte tem mais de uma com o msm nome. Não ainda artes com o mesmo nome, mas... Aguarde, pelo menos consigo avisar.')

    art = arts[0]

    name = art.name

    art = await art.edit(name=param[0])

    message = 'O nome da arte: **`{0}`** foi editado para: **`{1.name}`**'

    if art.type == 'RESPIRATION':
      message = 'A respiração chamada: **`{0}`** teve seu nome editado para: **`{1.name}`**'

    elif art.type == 'KEKKIJUTSU':
      message = 'O kekkijutsu chamado: **`{0}`** teve seu nome editado para: **`{1.name}`**'

    elif art.type == 'FIGHTING_STYLE':
      message = 'O estilo de luta chamado: **`{0}`** teve seu nome editado para: **`{1.name}`**'

    await ctx.send(message.format(name, art))

  @utils.flag(name='list', aliases=[ 'l' ])
  async def list(self, ctx: MorkatoContext, base: BaseType, param: ParamType) -> None: ...
  @utils.flag(name='attack', aliases=[ 'a' ])
  async def list(self, ctx: MorkatoContext, base: BaseType, param: ParamType) -> None:
    if not base:
      await ctx.send('Tá, mas qual é o nome?')

      return
    
    if not param:
      await ctx.send('Ok, mas qual ataque?')
    
    guild = ctx.morkato_guild

    art = guild.get_arts_by_name(base)[0]

    attacks = ctx.bot.database.attacks.where(guild=guild, art_id=art.id, name=param[0])

    attack = next(attacks, None)

    if not attack:
      await ctx.send('Essa ataque não existe nessa arte :/')

      return

    await ctx.send_attack(attack)