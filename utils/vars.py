from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from .types.vars import Variable as typedVariable
  from .guild import Guild  

class Variable:
  def __init__(self, guild: Guild, data: typedVariable) -> None:
    self.guild = guild

    self._load_variables(data)

  def __repr__(self) -> str:
    return f'${self.name}'
  
  def _load_variables(self, data: typedVariable) -> None:
    self.name = data['name']
    self.text = data['text']
    self.visibleCaseMemberNotThenRoles = data['visibleCaseIfNotAuthorizerMember']

    self.required_roles = data['required_roles']
    self.roles_id = data['roles']