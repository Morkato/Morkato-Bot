from typing import TypedDict, Optional, Literal

ArtType = Literal['RESPIRATION', 'KEKKIJUTSU', 'FIGHTING_STYLE']

class Art(TypedDict):
  name: str
  type: ArtType
  id: str

  embed_title:       Optional[str]
  embed_description: Optional[str]
  embed_url:         Optional[str]

  guild_id: str

  created_at: str
  updated_at: str