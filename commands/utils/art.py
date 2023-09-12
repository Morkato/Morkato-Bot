from typing import Union

from unidecode             import unidecode
from morkato.objects.types import ArtType

import re

def extract_art_type(text: str) -> Union[ArtType, None]:
  text = unidecode(text.strip())

  if re.match(r'r|resp|respiration|respiracao', text, re.IGNORECASE):
    return 'RESPIRATION'
  
  elif re.match(r'k|kekki|kkj|kekkijutsu', text, re.IGNORECASE):
    return 'KEKKIJUTSU'
  
  elif re.match(r'fs|fight-style', text, re.IGNORECASE):
    return 'FIGHTING_STYLE'
  

  
