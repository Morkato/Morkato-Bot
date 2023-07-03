"""
  Command utils: attack

  >> from .attack_utils import get
"""

from typing import Coroutine, Callable, Union, Any

from utils.string import Context
from utils.guild import Guild

async def get_attack(ctx: Context, guild: Guild, /) -> None:
  name = ctx.get_param('name')
  ctx.bot
  
  if not name:
    await ctx.send('QUal o nome mesmo?')

    return
  
  attack = guild.get_attack(name)

  if not attack:
    await ctx.send('Esse ataque não existe.')

    return

  await ctx.send(embed=attack.embed_at(ctx.author))

async def new_attack(ctx: Context, guild: Guild, /) -> None:
  name = ctx.get_param('name')
  art_name = ctx.get_param('value')

  if not art_name:
    await ctx.send('Pera, pera... Qual a arte mesmo?')

    return
  
  if not name:
    await ctx.send('Pera, pera... Qual o nome do ataque mesmo?')

    return

  art = guild.get_art(art_name)

  if not art:
    await ctx.send('Essa arte não existe.')

    return
  
  attack = art.new_attack(name)

  await ctx.send(f'Uma novo ataque chamado **`{attack}`** foi criado.')

async def edit_attack(ctx: Context, guild: Guild, /) -> None:
  name = ctx.get_param('name')

  if not name:
    await ctx.send('Pera, pera... Qual o nome do ataque mesmo?')

    return
  
  attack = guild.get_attack(name)

  if attack is None:
    await ctx.send('Esse ataque não existe.')

    return
  
  bot = ctx.bot
  
  payload = {}

  original_message = await ctx.send(embed=attack.embed_at())
  
  while True:
    message = await bot.wait_for('message', timeout=300, check=lambda message: message.author.id == ctx.author.id and message.channel.id == ctx.channel.id and message.guild.id == ctx.guild.id)

    content = message.content.strip()

    key, value = (content[:content.find('!')], content[content.find('!')+1:]) if not content.find('!') == -1 else (None, content)

    if key is None and value.lower() == 'done':
      if not payload:
        await ctx.send('Calma, calma. Ficando loco, o você não editou nada?')

        return
      
      attack.edit(**payload)

      await ctx.send('O ataque abordado foi editada.')

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
    
    elif key == 'damage':
      try: payload['damage'] = int(value)
      except:
        await message.add_reaction('❌')

        continue

      await message.add_reaction('✅')

    elif key == 'stamina':
      try:
        payload['stamina'] = int(value)
      except:
        await message.add_reaction('❌')

        continue

      await message.add_reaction('✅')
    else: continue
  
    await message.delete()

    original_message = await original_message.edit(embed=attack.embed_at(
      title=payload.get('embed_title'),
      description=payload.get('embed_description'),
      url=payload.get('embed_url'),
      damage=payload.get('damage'),
      stamina=payload.get('stamina'))
    )

async def del_attack(ctx: Context, guild: Guild, /) -> None:
  name = ctx.get_param('name')
  
  if not name:
    await ctx.send('Pera, pera... Qual o nome do ataque mesmo?')

    return

  attack = guild.get_attack(name)

  if not attack:
    await ctx.send('Esse ataque não existe.')

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
    attack = attack.delete()

    await ctx.send(f'O ataque com o nome **`{attack}`** foi deletado.')

attacks_flags = {
  'c': new_attack,
  'e': edit_attack,
  'd': del_attack,
  'DEFAULT': get_attack
}

def get(flag: str) -> Union[Callable[[Context, Guild], Coroutine[Any, Any, None]], None]:
  return attacks_flags.get(flag)