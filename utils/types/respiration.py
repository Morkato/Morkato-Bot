from typing import TypedDict, Literal, Union

class Respiration(TypedDict):
  name: str
  type: Literal['Respiration']
  role: Union[str, None]

  embed_title: Union[str, None]
  embed_description: Union[str, None]
  embed_url: Union[str, None]