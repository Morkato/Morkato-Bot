from __future__ import annotations
from aiohttp import ClientResponse
from enum import Enum
from typing import (
  Dict,
  Any
)

class MorkatoHTTPType(Enum):
  PLAYER_NOTFOUND = "PLAYER_NOTFOUND"
  PLAYER_ALREADYEXISTS = "PLAYER_ALREADYEXISTS"
  GENERIC = "GENERIC"
class ModelType(Enum):
  ABILITY = "ABILITY"
  FAMILY = "FAMILY"
  PLAYER = "PLAYER"
  ATTACK = "ATTACK"
  ART = "ART"
  NPC = "NPC"
  GENERIC = "GENERIC"
class MorkatoException(Exception):
  pass
class HTTPException(MorkatoException):
  def __init__(self, response: ClientResponse, extra: Dict[str, Any]):
    self.response: ClientResponse = response
    self.status: int = response.status
    self.extra = extra
class NotFoundError(HTTPException):
  def __init__(self, response: ClientResponse, model: ModelType, extra: Dict[str, Any]) -> None:
    super().__init__(response, extra)
    self.model = model
class PlayerNotFoundError(NotFoundError):
  def __init__(self, response: ClientResponse, extra: Dict[str, Any]) -> None:
    super().__init__(response, ModelType.PLAYER, extra)
class MorkatoServerError(HTTPException):
  pass