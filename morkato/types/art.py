from typing import TypedDict, Literal, Union

__all__ = (
  'ArtType',
  'Art'
)

ArtType = Literal['RESPIRATION', 'KEKKIJUTSU', 'FIGHTING_STYLE']

class Art(TypedDict):
  name: str
  type: ArtType
  id: str

  embed_title:       Union[str, None]
  embed_description: Union[str, None]
  embed_url:         Union[str, None]

  guild_id: str

  created_at: str
  updated_at: str