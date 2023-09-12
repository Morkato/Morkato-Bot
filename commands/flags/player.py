from typing import (
  Literal,
  Union
)

from ..ext  import Command, message_page_embeds, flag

from discord.ext   import commands
from morkato.objects.guild import Guild

from morkato.objects.types.player import PlayerBreed

import discord
import re

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

    appearance = params.get('image')

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

    if appearance:
      rest['appearance'] = appearance

    player = await guild.create_player(
      id=str(member.id),
      name=name,
      breed=breed,
      **rest
    )

    await ctx.send(f'**`{member.name}`** foi registrado.')

  @flag(name='setName')
  async def setName(self, ctx: commands.Context, guild: Guild, member: discord.Member, name: Union[str, None], /) -> None:
    player = guild.get_player(id=str(member.id))

    if not name:
      await ctx.send('Beleza, mas vou trocar para qual nome?')

      return
    
    player = await player.edit(name=name)

    await ctx.send(f'O nome do **{member.name}** foi alterado para: **`{player.name}`**')
  
  @flag(name='setLife')
  async def setLife(self, ctx: commands.Context, guild: Guild, member: discord.Member, life: Union[str, None], /) -> None:
    player = guild.get_player(id=str(member.id))

    if not life:
      await ctx.send('Hmmmmmmm, okok, não irei colocar nenhuma vida.')

      return
    
    if not re.match(r'[0-9]+', life.strip()):
      await ctx.send('Apenas números, ok?')

      return
    
    player = await player.edit(life=int(life))

    await ctx.send(f'A vida do **`{member.name}`** foi alterada para: **`{player.life}`**')

  @flag(name='setCredibility')
  async def setCredibility(self, ctx: commands.Context, guild: Guild, member: discord.Member, credibility: Union[str, None], /) -> None:
    player = guild.get_player(id=str(member.id))

    if not credibility:
      await ctx.send('Eu não sei se li direito, mas acho que você não colocou nenhuma credibilidade :/', tts=True)

      return
    
    if not re.match(r'[0-9]+', credibility.strip()):
      await ctx.send('Apenas números, ok?')

      return
    
    player = await player.edit(credibility=int(credibility))

    await ctx.send(f'A credibilidade do **`{member.name}`** foi alterada para **`{player.credibility}`**.')
  
  @flag(name='setBreath')
  async def setBreath(self, ctx: commands.Context, guild: Guild, member: discord.Member, breath: Union[str, None], /) -> None:
    player = guild.get_player(id=str(member.id))

    if not breath:
      await ctx.send(f'Bem, não entendi. Cadê o fôlego?')

      return
    
    if not re.match(r'[0-9]+', breath.strip()):
      await ctx.send('Apenas números, ok?')
      
      return
    
    player = await player.edit(breath=int(breath))
    
    await ctx.send(f'O fôlego do **`{member.name}`** foi alterado para **`{player.breath}`**.')

  @flag(name='setBlood')
  async def setBlood(self, ctx: commands.Context, guild: Guild, member: discord.Member, blood: Union[str, None], /) -> None:
    player = guild.get_player(id=str(member.id))

    if not blood:
      await ctx.send('Bem, você especificou o sangue?')
      
      return
    
    if not re.match(r'[0-9]+', blood.strip()):
      await ctx.send('Apenas números, ok?', ephemeral=True)
      
      return
    
    player = await player.edit(blood=blood)

    await ctx.send(f'O sangue do **`{member.name}`** foi alterado para **`{player.blood}`**.')

  @flag(name='setAppearance')
  async def setAppearance(self, ctx: commands.Context, guild: Guild, member: discord.Member, uri: Union[str, None], /) -> None:
    player = guild.get_player(id=str(member.id))

    if not uri:
      await ctx.send('Ok, cadê a nova url?')
      
      return
    
    uri = uri.strip()
    
    if not re.match(r'^(http://|https://)?[a-zA-Z0-9]+([\-\.]{1}[a-zA-Z0-9]+)*\.[a-zA-Z]{2,5}(:[0-9]{1,5})?(/.*)?$', uri):
      await ctx.send('Apenas links, ok?')

      return
    
    player = await player.edit(appearance=uri)

    await ctx.send(f'A aparência do **`{member.name}`** foi alterada.')
    