from typing import (
  Literal,
  Union
)

from io import BytesIO

from .utils       import reaction_checker, message_checker

from ..ext  import Command, message_page_embeds, flag

from discord.ext   import commands
from morkato.objects.guild import Guild

from morkato.errors import NotFoundError

import discord

FlagChecker = Literal['author', 'guild', 'channel', 'message']

class AttackCommand(Command):
  @flag(name='default', aliases=['info'])
  async def default(self, ctx: commands.Context, guild: Guild, member: discord.Member, name: Union[str, None], /) -> None:
    if not name:
      await ctx.send('Pera, pera... Qual o nome mesmo? Sumiu T-T')

      return
    
    attack = guild.get_attacks_by_name(name)[0]

    player = None

    try:
      player = guild.get_player(str(member.id))
    except NotFoundError: ...
    
    embed = await attack.embed_at()

    if not player:
      await ctx.send(f'{member.name} Você não possui registro.', embed=embed)

      return

    embed.set_author(name=player.name, icon_url=player.appearance or member.display_avatar.url)
    
    await ctx.send(embed=embed)
  
  @flag(name='create', aliases=['c', 'new'])
  async def create(self, ctx: commands.Context, guild: Guild, util, name: Union[str, None], art_name: Union[str, None], /) -> None:
    if not name:
      await ctx.send('Beleza tô criando e..... Cadê o nome?!')

      return
    
    art = None
    
    if art_name:
      art = guild.get_art_by_name(art_name)[0]

    attack = await guild.create_attack(name=name, art=art)

    message = 'Um novo ataque com o nome: **`{0.name}`** foi criado'
    
    if not art:
      await ctx.send(message.format(attack))

      return
    
    if art.type == 'RESPIRATION':
      message = 'Um novo ataque com o nome: **`{0.name}`** foi criado na respiração: **`{1.name}`**'

    elif art.type == 'KEKKIJUTSU':
      message = 'Um novo ataque com o nome: **`{0.name}`** foi criado no kekkijutsu: **`{1.name}`**'
    
    await ctx.send(message.format(attack, art))
  
  @flag(name='edit', aliases=['e'])
  async def edit(self, ctx: commands.Context, guild: Guild, util, name: Union[str, None], /) -> None:
    if not name:
      await ctx.send('Me pergunto: "Como vou editar algo sem nome"?')

      return

    attack = guild.get_attacks_by_name(name)[0]

    embed = await attack.embed_at()

    payload = {}

    original_message = await ctx.send(embed=embed)

    bot: commands.Bot = ctx.bot
    
    while True:
      message = await bot.wait_for('message', timeout=300, check=message_checker(ctx, [ 'author', 'channel', 'guild' ]))

      prefix_index = message.content.find('!')

      prefix, content = (None, message.content) if prefix_index == -1 else (message.content[:prefix_index].lower(), message.content[prefix_index+1:])

      if prefix is None and content.lower() == 'done':
        if not payload:
          await ctx.send('Pera, pera... Ficando loco, ou você não editou nada?')

          return
        
        attack = await attack.edit(
          title=payload.get('title'),
          description=payload.get('description'),
          url=payload.get('url')
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

  @flag(name='rename', aliases=['r', 'setname'])
  async def rename(self, ctx: commands.Context, guild: Guild, util, name: Union[str, None], to_name: Union[str, None], /) -> None:
    if not name:
      await ctx.send('Pera, pera... Qual o nome mesmo? Sumiu T-T')

      return
    
    if not to_name:
      await ctx.send('Ok, irei editar o nome para... Hã... Qual nome?')

      return
    
    attack = guild.get_attack_by_name(name)

    name = attack.name

    attack = await attack.edit(name=to_name)

    await ctx.send(f'O ataque chamado: **`{name}`** foi editado para: **`{attack.name}`**')

  @flag(name='delete', aliases=['d'])
  async def delete(self, ctx: commands.Context, guild: Guild, util, name: Union[str, None], /) -> None:
    if not name:
      await ctx.send('Pera, pera... Qual o nome mesmo? Sumiu T-T')

      return
    
    attack = guild.get_attack_by_name(name)

    embed = await attack.embed_at()
    
    message = await ctx.send('Tem certeza?', embed=embed)

    await message.add_reaction('✅')
    await message.add_reaction('❌')

    bot: commands.Bot = ctx.bot # type: ignore
    
    reaction, user = await bot.wait_for('reaction_add', timeout=20, check=reaction_checker(ctx, message, [ 'author', 'guild', 'channel', 'message' ]))
    
    if str(reaction.emoji) == '✅':
      attack = await attack.delete()

      await ctx.send(f'O ataque com o nome: **`{attack.name}`** foi deletado.')
    
    elif str(reaction.emoji) == '❌':
      await ctx.send('Ok, você mudou de ideia.')
  
  @flag(name='list', aliases=['l'])
  async def list(self, ctx: commands.Context, guild: Guild, util, art_name: Union[str, None], /) -> None:
    nick = 'Anonymous'
    avatar = None

    try:
      player = guild.get_player(str(ctx.author.id))

      nick = player.name
      avatar = player.appearance or ctx.author.display_avatar.url
    
    except NotFoundError: pass
    
    db = guild.client.database

    art = None

    if art_name:
      art = guild.get_art_by_name(art_name)[0]

    attacks = list(db.attacks.where(art=art))

    embeds = [ (await attack.embed_at()).set_author(name=nick, icon_url=avatar) for attack in attacks]

    await message_page_embeds(ctx, ctx.bot, embeds)
  
  @flag(name='attr', aliases=['a'])
  async def attr(self, ctx: commands.Context, guild: Guild, util, name: Union[str, None], attr: Union[str, None], /) -> None:
    if not name:
      await ctx.send('Pera, pera... Qual o nome mesmo? Sumiu T-T')

      return
    
    attack = guild.get_attack_by_name(name)

    if not attr:
      await ctx.send(f'**`{attack}`**')

      return
    
    attr = getattr(attack, attr, 'Esse atributo não existe.')

    await ctx.send(attr)
