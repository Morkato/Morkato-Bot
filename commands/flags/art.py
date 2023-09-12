from typing import (
  Literal,
  Union,

  List
)

from ..ext  import Command, message_page_embeds, flag
from .utils import reaction_checker, message_checker

from discord.ext       import commands
from morkato.objects.types.art import ArtType
from morkato.objects.guild     import Guild

import re

RESPIRATION_PATTERN = r'RESPIRATION|RESP|R'
KEKKIJUTSU_PATTERN  =  r'KEKKIJUTSU|KEKKI|KKJ|K'

def extract_art_type(text: str) -> Union[ArtType, None]:
  if re.match(RESPIRATION_PATTERN, text, re.IGNORECASE):
    return 'RESPIRATION'
  
  elif re.match(KEKKIJUTSU_PATTERN, text, re.IGNORECASE):
    return 'KEKKIJUTSU'

class ArtCommand(Command):
  @flag(name='default', aliases=['info'])
  async def default(self, ctx: commands.Context, guild: Guild, util, name: Union[str, None]) -> None:
    if not name:
      await ctx.send('Ok, procurando, procurando...Pera, pera! Cadê o nome?? Eu estava procurando o que?? Agora que vi '-'')

      return
    
    arts = guild.get_arts_by_name(name)

    art = arts[0]

    embeds = await art.embed_at()

    await message_page_embeds(ctx, ctx.bot, embeds)

  @flag(name='create', aliases=['c', 'new'])
  async def create(self, ctx: commands.Context, guild: Guild, util, name: Union[str, None], art_type: Union[str, None]) -> None:
    flag = self.create.name
    
    if not name:
      await ctx.send('Vamos lá, irei criar a nova arte, mas... Cadê o nome?')

      return
    
    if not art_type:
      await ctx.send(f'É necessário especificar o tipo, exemplo: ``` !art --{flag} {name} -- RESPIRATION ``` ou ``` !art --{flag} {name} -- KEKKIJUTSU ```')

      return
    
    type = extract_art_type(art_type)

    if not type:
      await ctx.send(f'Somente os tipos: **`RESPIRATION`** ou **`KEKKIJUTSU`**, exemplo: ``` !art --{flag} {name} -- RESPIRATION ``` ou ``` !art --{flag} {name} -- KEKKIJUTSU ```')

      return
    
    art = await guild.create_art(name=name, type=type)

    message = 'Uma nova arte chamada: **`{0.name}`** foi criada.'

    if art.type == 'RESPIRATION':
      message = 'Uma nova respiração com o nome: **`{0.name}`** foi criada.'

    if art.type == 'KEKKIJUTSU':
      message = 'Um novo kekkijutsu com o nome: **`{0.name}`** foi criado.'

    await ctx.send(message.format(art))
  
  @flag(name='edit', aliases=['e'])
  async def edit(self, ctx: commands.Context, guild: Guild, util, name: Union[str, None]) -> None:
    if not name:
      await ctx.send('Ok, vamos editar a arte sem nome... Pera, ela não tem nome.')

      return
    
    art = guild.get_art_by_name(name)[0]

    embeds = await art.embed_at()
    embed = embeds[0]

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
  
  @flag(name='rename', aliases=['r', 'setname'])
  async def rename(self, ctx: commands.Context, guild: Guild, util, name: Union[str, None], to_name: Union[str, None], /) -> None:
    if not name:
      await ctx.send('Bem, vamos trocar o nome do nada para... Hâ... Pera, como vou saber qual arte trocar sem o nome?!')

      return
    
    if not to_name:
      await ctx.send('Beleza, vamos editar o nome para nenhum nome?.. Tá certo isso??')
      
      return
    
    art = guild.get_art_by_name(name)[0]

    name = art.name

    art = await art.edit(name=to_name)

    message = 'O nome da arte: **`{0}`** foi editado para: **`{1.name}`**'

    if art.type == 'RESPIRATION':
      message = 'A respiração chamada: **`{0}`** teve seu nome editado para: **`{1.name}`**'

    elif art.type == 'KEKKIJUTSU':
      message = 'O kekkijutsu chamado: **`{0}`** teve seu nome editado para: **`{1.name}`**'

    await ctx.send(message.format(name, art))

  @flag(name='delete', aliases=['d'])
  async def delete(self, ctx: commands.Context, guild: Guild, util, name: Union[str, None]) -> None:
    if not name:
      await ctx.send('Irei apagar a arte com o nome --- cadê o nome??')

      return
    
    art = guild.get_art_by_name(name)[0]

    embeds = await art.embed_at()

    embed = embeds[0]
    
    message = await ctx.send('Tem certeza?', embed=embed)

    await message.add_reaction('✅')
    await message.add_reaction('❌')

    bot: commands.Bot = ctx.bot # type: ignore
    
    reaction, user = await bot.wait_for('reaction_add', timeout=20, check=reaction_checker(ctx, message, [ 'author', 'guild', 'channel', 'message' ]))
    
    if str(reaction.emoji) == '✅':
      art = await art.delete()

      message = 'A arte com o nome: **`{0.name}`** foi deletada.'

      if art.type == 'RESPIRATION':
        message = 'A respiração chamada: **`{0.name}`** foi deletada.'

      elif art.type == 'KEKKIJUTSU':
        message = 'O kekkijutsu chamado: **`{0.name}`** foi deletado.'
      
      await ctx.send(message.format(art))
    
    elif str(reaction.emoji) == '❌':
      await ctx.send('Ok, você mudou de ideia.')
  
  @flag(name='list', aliases=['l'])
  async def list(self, ctx: commands.Context, guild: Guild, util, by: Union[str, None]) -> None:
    if by:
      by = extract_art_type(by)

      if not by:
        await ctx.send('Apenas os tipos: **`RESPIRATION`** ou **`KEKKIJUTSU`**')

        return
      
    list_by = by or None

    arts = list(guild.arts.where(type=list_by))

    await ctx.send(f'**`{arts}`**')

