from typing import (
  Literal,
  Union
)

from .utils import reaction_checker, message_checker
from ..ext  import Command, message_page_embeds, flag

from discord.ext   import commands
from objects.guild import Guild

from objects.types.player import PlayerBreed

import discord

FlagChecker = Literal['author', 'guild', 'channel', 'message']

def extractBreed(text: str) -> Union[PlayerBreed, None]:
  text = text.lower().strip()

  if text in ('human', 'humano', 'hu'):
    return 'HUMAN'
  
  elif text in ('oni', 'o'):
    return 'ONI'
  
  elif text in ('hybrid', 'híbrido', 'hibrido', 'hi'):
    return 'HYBRID'

class PlayerCommand(Command):
  @flag(name='default')
  async def default(self, ctx: commands.Context, guild: Guild, member: discord.Member, attr: Union[str, None], /) -> None:
    player = guild.get_player(str(member.id))

    if not attr:
      file = discord.File(await player.card(member), filename='card.png')

      await ctx.send(file=file)
      
      return
    
    await ctx.send(str(getattr(player, attr, None)))
  
  @flag(name='register', aliases=['r'])
  async def register(self, ctx: commands.Context, guild: Guild, member: discord.Member, name: Union[str, None], value_in, params: dict[str, str], /) -> None:
    if member.bot:
      await ctx.send('Não posso registrar um bot \'-\'.')

      return
    
    if not name:
      await ctx.send(f'É necessário especificar o nome.')

      return
    
    breed = params.get('breed')

    if not breed:
      await ctx.send(f'É necessário especificar a raça.')

      return
    
    breed = extractBreed(breed)

    if not breed:
      await ctx.send(f'Essa raça nn existe.')

      return
    
    life = params.get('life')
    credibility = params.get('credibility')
    breath = params.get('breath')
    blood = params.get('blood')
    cash = params.get('cash')
    exp = params.get('exp')

    rest = {  }

    if life:
      rest['life'] = int(life)

    if credibility:
      rest['credibility'] = int(credibility)
    
    if breath:
      rest['breath'] = int(breath)
    
    if blood:
      rest['blood'] = int(blood)

    if cash:
      rest['cash'] = int(cash)

    if exp:
      rest['exp'] = int(exp)

    player = await guild.create_player(
      id=str(member.id),
      name=name,
      breed=breed,
      **rest
    )

    await ctx.send(f'**`{member.name}`** foi registrado.')


    