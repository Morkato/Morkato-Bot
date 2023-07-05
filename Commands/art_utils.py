"""
  Command utils: art

  >> from .art_utils import get
"""

from typing import Callable, Coroutine, Literal, Union, Any

from utils.commands import message_page_embeds

from utils.string import Context
from utils.guild import Guild

def get_filtered_type(text: str) -> Union[Literal[
  'RESPIRATION',
  'KEKKIJUTSU'
], None]:
  text = text.lower()

  if text in [ 'r', 'respiration', 'resp' ]:
    return 'RESPIRATION'

  elif text in [ 'k', 'kekkijutsi', 'kekki' ]:
    return 'KEKKIJUTSU'

async def get_art(ctx: Context, guild: Guild, /) -> None:
  name = ctx.get_param('name')

  if not name:
    await ctx.send('Pera, pera, qual o nome da arte mesmo?')

    return
  
  art = guild.get_art(name)

  if not art:
    await ctx.send('Essa arte não existe')

    return
  
  await message_page_embeds(ctx, ctx.bot, art.embeds)

async def new_art(ctx: Context, guild: Guild, /) -> None:
  flag = ctx.get_param('param')

  name = ctx.get_param('name')
  art_type = ctx.get_param('value')

  if not name:
    await ctx.send('Pera, pera, qual o nome da arte mesmo?')
    
    return
  
  if not art_type:
    await ctx.send(f'É necessário especificar o tipo,, por exemplo: **```!art -{flag} {name} > respiration``` ou: ```!art -{flag} {name} > kekkijutsu```**')

    return
  
  art_type = get_filtered_type(art_type)
  
  if not art_type:
    await ctx.send(f'Somente esses os tipos `RESPIRATION` ou `KEKKIJUTSU`, por exemplo: **```!art -{flag} {name} > respiration``` ou: ```!art -{flag} {name} > kekkijutsu```**')
    
    return
  
  art = guild.new_art(name=name, type=art_type)

  if art_type == 'RESPIRATION':
    await ctx.send(f'Uma nova respiração com o seguinte nome: **`{art.name}`** foi criada!')

    return
  
  if art_type == 'KEKKIJUTSU':
    await ctx.send(f'Um novo kekkijutsu com o seguinte nome: **`{art.name}`** foi criado!')

    return
  
  await ctx.send(f'Uma nova arte com o seguinte nome: **`{art.name}`** foi criada!')

async def edit_art(ctx: Context, guild: Guild, /) -> None:
  name = ctx.get_param('name')

  if not name:
    await ctx.send('Como irei saber qual arte editar sem o nome?')

    return

  art = guild.get_art(name)

  if not art:
    await ctx.send('Essa arte não existe.')

    return

  payload = {}

  original_message = await ctx.send(embed=art.embeds[0])

  bot = ctx.bot

  while True:
    message = await bot.wait_for('message', timeout=300, check=lambda message: message.author.id == ctx.author.id and message.channel.id == ctx.channel.id and message.guild.id == ctx.guild.id)

    content = message.content.strip()

    key, value = (content[:content.find('!')], content[content.find('!')+1:]) if not content.find('!') == -1 else (None, content)

    if key is None and value.lower() == 'done':
      if not payload:
        await ctx.send('. . ? Tô ficando loco, ou você não editou nada mesmo?')

        return
      
      art.edit(**payload)

      await ctx.send('A arte abordada foi editada.')

      return
    
    elif key == 'title':
      payload['embed_title'] = value

      await message.add_reaction('✅')

    elif key == 'description':
      payload['embed_description'] = value

      await message.add_reaction('✅')

    elif key == 'url':
      payload['embed_url'] = value

      await message.add_reaction('✅')

    await message.delete()

    embed = art.embed_at(
      title=payload.get('embed_title'),
      description=payload.get('embed_description'),
      url=payload.get('embed_url')
    )

    original_message = await original_message.edit(embed=embed)

async def del_art(ctx: Context, guild: Guild) -> None:
  name = ctx.get_param('name')  

  if not name:
    await ctx.send('Como deletar uma arte sem nome?')

    return

  bot = ctx.bot
  
  message = await ctx.send('Você tem certeza que deseja apagar esse ataque?')

  await message.add_reaction('✅')
  await message.add_reaction('❌')

  reaction, user = await bot.wait_for('reaction_add', timeout=20, check=lambda reaction, user: (
    user.id == ctx.author.id
    and reaction.message.channel.id == ctx.channel.id
    and message.id == reaction.message.id
  ))
  
  if str(reaction.emoji) == '✅':
    art = guild.del_art(name)

    await ctx.send(f'A arte com o nome **`{art.name}`** foi deletada.')

async def list_art(ctx: Context, guild: Guild, /) -> None:
  list_by = ctx.get_param('name')
  flag = ctx.get_param('param')

  if not list_by:
    await ctx.send(f'Listando por nada: **`{guild.arts[:10]}`**')

    return
  
  list_by = get_filtered_type(list_by.strip())
  
  if not list_by:
    await ctx.send(f'Somente esses os tipos `RESPIRATION` ou `KEKKIJUTSU`, por exemplo: **```!art -{flag} respiration``` ou: ```!art -{flag}  kekkijutsu```**')
    
    return
  
  arts = guild.get_arts(map=list_by)

  await ctx.send(f'Listando por `{list_by}`: **`{arts[:10]}`**')

async def charge_name(ctx: Context, guild: Guild, /) -> None:
  after, before = (ctx.get_param('name'), ctx.get_param('value'))

  if not after:
    await ctx.send('Como editar o nome do "nada"?')

    return
  
  if not before:
    await ctx.send('Ok, irei editar o nome para... Hã.? Que nome?')

    return
  
  art = guild.get_art(after)

  if not art:
    await ctx.send('Como trocar o nome de uma arte que não existe?')

    return
  
  art.edit(name=before)

  await ctx.send(f'O nome dá **`{after}`** foi alterado para **`{before}`**.')

flags = {
  'DEFAULT': get_art,
  'c': new_art,
  'e': edit_art,
  'd': del_art,
  'l': list_art,
  'n': charge_name
}

def get(flag: str) -> Union[Callable[[Context, Guild], Coroutine[Any, Any, None]], None]:
  return flags.get(flag)