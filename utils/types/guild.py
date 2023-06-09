from typing import TypedDict, List
from .vars import Variable

class Guild(TypedDict):
  id: str

  vars: List[Variable]

  created_at: str
  updated_at: str