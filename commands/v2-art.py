from typing import Union, Dict, List

from morkato.converters import CommandConverter
from .                  import utils
from morkato            import (
  MorkatoBot,
  MorkatoContext,
  Cog
)

from discord.ext import commands

import re

class Art(Cog, name='v2-Art'):
  async def process_params(self, ctx: MorkatoContext, base: Union[str, None], params: Dict[str, List[str]]) -> None:
    if not params:
      return
    
    guild = ctx.morkato_guild
    
    key, value = next(iter(params.items()))

    key = key.strip()

    if re.match(r'c|create', key):
      if not base:
        await ctx.send('Tá bom, mas qual o tipo? Respiração, kekkijutsu, estilo de luta, qual?')

        return
      
      base = utils.extract_art_type(base)

      if not base:
        await ctx.send('Ok, mas que tipo de arte é esse?')

        return
      
      if not value:
        await ctx.send('Ok, irei criar quantas artes hoje?')

        return
      
      arts = [ await guild.create_art(name=name, type=base) for name in value ]
      
      await ctx.send('\n'.join(
        f'Foi criado um novo kekkijutsu chamado: **`{art.name}`**'
        if art.type == 'KEKKIJUTSU'
        else (
          f'Foi criada um nova respiração chamada: **`{art.name}`**'
          if art.type == 'RESPIRATION'
          else (
            f'Foi criado um novo estilo de luta chamado: **`{art.name}`**'
            if art.type == 'FIGHTING_STYLE'
            else f'Foi criado uma nova arte, chamada: **`{art.name}`**'
          )
        ) for art in arts))

  @commands.command(name='v2-art')
  async def art(self, ctx: MorkatoContext, *, cmd: CommandConverter) -> None:
    guild = ctx.morkato_guild
    
    if not cmd.params:
      if not cmd.base:
        await ctx.send('Tá, mas qual é o nome?')

        return
      
      arts = guild.get_arts_by_name(cmd.base)

      art = arts[0]

      await ctx.send_art(art)
      
      return
    
    await self.process_params(ctx, cmd.base, cmd.params)
    
async def setup(bot: MorkatoBot) -> None:
  await bot.add_cog(Art(bot))