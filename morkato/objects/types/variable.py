from typing import TypedDict, List

class Variable(TypedDict):
  name:                             str
  text:                             str
  visibleCaseIfNotAuthorizerMember: bool

  required_roles: int
  roles:          List[str]

  created_at: str
  updated_at: str