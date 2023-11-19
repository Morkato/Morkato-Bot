from __future__ import annotations

from typing import Optional, Generator, TypeVar, Union, overload, List, TYPE_CHECKING, Any

if TYPE_CHECKING:
  from .. import Art, ArtType

from unidecode import unidecode
from itertools import zip_longest

import discord
import re

LIMIT_PAGE = 10

T = TypeVar('T')

def extract_art_type(text: str) -> Union[ArtType, None]:
  text = unidecode(text.strip())

  if re.match(r'r|resp|respiration|respiracao', text, re.IGNORECASE):
    return 'RESPIRATION'
  
  elif re.match(r'k|kekki|kkj|kekkijutsu', text, re.IGNORECASE):
    return 'KEKKIJUTSU'
  
  elif re.match(r'fs|fight-style', text, re.IGNORECASE):
    return 'FIGHTING_STYLE'

def organize_arts(arts: List[Art], by: Optional[ArtType] = None):
  fields = []

  if by:
    arts = [art for art in arts if art.type == by]

    fields = ({
      'name': ("Respirações" if by == 'RESPIRATION' else ('Kekkijutsus' if by == 'KEKKIJUTSU' else 'Estilos de Luta')),
      'value': '\n'.join((
        f"**{i}°** - Respiração: "
        if by == 'RESPIRATION'
        else (
          f'**{i}°** - Kekkijutsu: '
          if by == 'KEKKIJUTSU'
          else f"**{i}°** - Estilo de Luta: "
        )
      ) + f'**`{art.name}`**' for i, art in enumerate(arts[idx:idx+LIMIT_PAGE], start=idx+1)),
      'inline': False
    } for idx in range(0, len(arts), LIMIT_PAGE))

    for field in fields:
      yield discord.Embed(
        title=("Respirações" if by == 'RESPIRATION' else ('Kekkijutsus' if by == 'KEKKIJUTSU' else 'Estilos de Luta')),
        description="..."
      ).add_field(**field)
    
    return
  
  embeds_respiration = organize_arts(arts, 'RESPIRATION')
  embeds_kekkijutsu = organize_arts(arts, 'KEKKIJUTSU')
  embeds_fight_style = organize_arts(arts, 'FIGHTING_STYLE')

  for emb_resp, emb_kekki, emb_fight in zip_longest(embeds_respiration, embeds_kekkijutsu, embeds_fight_style, fillvalue=None):
    embed = discord.Embed(
      title='Artes',
      description='Artes são técnicas em nosso RPG para generalizar: Respirações, Kekkijutsus e Estilos de luta. Com ela, fica tudo compacto em um comando, tanto as respirações, que são técnicas usadas por caçadores de demônios, em que cada uma  tem características e habilidades únicas; os kekkijutsus que são técnicas sobrenaturais que são desenvolvidas por onis e estilos de luta, que como o próprio nome sugere, são estilos de combate específicos, feito por personagens ao longo da trama.'
    )

    if not hasattr(embed, '_fields'):
      embed._fields = []
    

    if emb_resp:
      embed._fields += emb_resp._fields

    if emb_kekki:
      embed._fields += emb_kekki._fields

    if emb_fight:
      embed._fields += emb_fight._fields
    
    yield embed
