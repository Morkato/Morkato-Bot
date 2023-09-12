from __future__ import annotations

from typing import TYPE_CHECKING, List

from .types import variable

if TYPE_CHECKING:
  from morkato.api import MorkatoAPIController
  
  from .guild import Guild

class Variable:
  def __init__(
    self, *,
    http:    MorkatoAPIController,
    guild:   Guild,
    payload: variable.Variable
  ) -> None:
    self.http  = http
    self.guild = guild

    self._load_variables(payload)
  
  def _load_variables(self, payload: variable.Variable) -> None:
    self.__name    = payload['name']
    self.__text    = payload['text']    

    self.__required_roles = payload['required_roles']
    self.__roles_id       = payload['roles']

  @property
  def name(self) -> str:
    return self.__name
  
  @property
  def text(self) -> str:
    return self.__text
  
  @property
  def required_roles(self) -> int:
    return self.__required_roles
  
  @property
  def roles_id(self) -> List[str]:
    return self.__roles_id
