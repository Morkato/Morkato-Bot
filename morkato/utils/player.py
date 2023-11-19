from ..types.player import PlayerBreed
from .etc           import strip_text

from ..errors import ValidationError

import re

def extract_player_breed(text: str) -> PlayerBreed:
  text = strip_text(text, ignore_accents=True, case_insensitive=True, strip_text=True, ignore_empty=True)

  if re.match(r'hu|humano|human', text, re.IGNORECASE):
    return 'HUMAN'
  
  elif re.match(r'o|oni', text, re.IGNORECASE):
    return 'ONI'
  
  elif re.match(r'hy|hybrid|hibrido', text, re.IGNORECASE):
    return 'HYBRID'
  
  raise ValidationError