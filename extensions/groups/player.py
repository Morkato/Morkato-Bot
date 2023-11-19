from typing import (
  Union,

  List,
  Dict
)

from discord.ext import commands
from morkato     import (
  MorkatoContext,
  
  errors,
  utils
)

BaseType = Union[str, None]
ParamType = List[str]
ParametersType = Dict[str, ParamType]

class PlayerGroupFlag(utils.FlagGroup):
  @utils.flag(aliases=['r'])
  async def register(self, ctx: MorkatoContext, base: BaseType, param: ParamType, params: ParametersType) -> None:
    member = ctx.author
      
    if base:
      member = await commands.MemberConverter().convert(ctx, base)

    try:
      ctx.morkato_guild.get_player(member)

      if ctx.author.id == member.id:
        await ctx.send('Cara, você já possui registro \'-\'')

        return
      
      await ctx.send('Esse usuário já possui registro :/')

      return
    except errors.NotFoundError: pass

    if not param:
      await ctx.send(f'Beleza, mas esse mano aí não tem nome não? Sério? Acho que você esqueceu, bem, se eu quero chamá-lo de "Jão; O mito" eu daria o comando: **``` !{ctx.command.name} {member.id} --{self.register.name} Jão; O mito ```**')

      return
    
    name = param[0]
    
    breed = params.get('B', None)

    if not breed:
      await ctx.send(f'É necessário especificar a raça da pessoa, por exemplo: **``` !{ctx.command.name} {member.id} --{self.register.name} {name} -B [breed] ```** Substituindo `[breed]` por: `HUMAN`, `ONI` ou `HYBRID`')

      return
    
    try:
      breed = utils.extract_player_breed(breed[0])
    except errors.ValidationError:
      await ctx.send(f'Apenas os tipos: `HUMAN`, `ONI` ou `HYBRID`. Por exemplo, quero criar um humano: **``` !{ctx.command.name} {member.id} --{self.register.name} {name} -B Humano ```**')
      
      return
    
    """
      [?] Optional Flags!

      -L - Life
      -C - Credibility
      -H - History
      -S - Blood
      -F - Breath
      -R - Resistance
      -V - Velocity
      -A - Appearance URI
    """

    payload = {  }
    
    if params.get('L'):
      payload['life'] = int(params['L'][-1])

    if params.get('C'):
      payload['credibility'] = int(params['C'][-1])

    if params.get('H'):
      payload['history'] = int(params['H'][-1])
    
    if params.get('S'):
      payload['blood'] = int(params['S'][-1])
    
    if params.get('F'):
      payload['breath'] = int(params['F'][-1])

    if params.get('R'):
      payload['resistance'] = int(params['R'][-1])
    
    if params.get('V'):
      payload['velocity'] = int(params['V'][-1])
    
    if params.get('A'):
      payload['appearance'] = params['A'][-1]
    
    player = await ctx.morkato_guild.create_player(id=member.id, name=name, breed=breed, **payload)

    await ctx.send(f'**`@{member.name}`** foi registrado com sucesso!')
  
  @utils.flag(aliases=['ur', 'd', 'delete'])
  async def unregister(self, ctx: MorkatoContext, base: BaseType, param: ParamType) -> None:
    member = ctx.author

    if base or param:
      member = await commands.MemberConverter().convert(ctx, base or param[0])

    try:
      player = ctx.morkato_guild.get_player(member)

      message = await ctx.send(f'Você tem certeza que deseja apagar o personagem de: **`@{member.name}`** chamado: **`{player.name}`**?')

      await message.add_reaction('✅')
      await message.add_reaction('❌')

      reaction, user = await ctx.bot.wait_for('reaction_add', timeout=20, check=utils.reaction_checker(ctx, message, [ 'author', 'channel', 'guild', 'message' ]))

      if str(reaction.emoji) == '✅':
        player = await player.delete()

        await ctx.send(f'O personagem do **`@{member.name}`** chamado: **`{player.name}`** foi deletado.')
      
      elif str(reaction.emoji) == '❌':
        await ctx.send('Ainda bem que tem um aviso para nós pensarmos duas vezes antes né não?')

    except errors.NotFoundError:
      if member.id == ctx.author.id:
        await ctx.send('Como vou deletar seu personagem se tu não tem um personagem? :/')

        return
      
      await ctx.send(f'Como vou deletar o personagem do: **`@{member.name}`** se ele não tem personagem? :V')
  
  @utils.flag(aliases=['e'])
  async def edit(self, ctx: MorkatoContext, base: BaseType, param: ParamType, params: ParametersType) -> None:
    member = ctx.author

    if base:
      member = await commands.MemberConverter().convert(ctx, base)

    try:
      player = ctx.bot.database.get_player(member)

      payload = {  }

      if param:
        print(param)
        payload['name'] = param[-1]

      if params.get('setLife'):
        payload['life'] = int(params['setLife'][-1])
      
      if params.get('setCredibility'):
        payload['credibility'] = int(params['setCredibility'][-1])

      if params.get('setHistory'):
        payload['history'] = int(params['setHistory'][-1])
      
      if params.get('setBlood'):
        payload['blood'] = int(params['setBlood'][-1])
      
      if params.get('setBreath'):
        payload['breath'] = int(params['setBreath'][-1])

      if params.get('setResistance'):
        payload['resistance'] = int(params['setResistance'][-1])
      
      if params.get('setVelocity'):
        payload['velocity'] = int(params['setVelocity'][-1])
      
      if params.get('setAppearance'):
        payload['appearance'] = params['setAppearance'][-1]

      if params.get('setBanner'):
        payload['banner'] = params['setBanner'][-1]

      if not payload:
        await ctx.send('Pera aí, tô doido, ou tu nn editou nada?')

        return

      print(payload)
      
      player = await player.edit(**payload)

      await ctx.send(f'O personagem do **`@{member.name}`** foi editado com sucesso.')

    except errors.NotFoundError:
      if ctx.author.id == member.id:
        await ctx.send('Pera, pera, como vou editar seu personagem se ele não existe?')

        return
      
      await ctx.send('Calmou, espera... Como vou editar u7m personagem que não existe, pera, que.')
