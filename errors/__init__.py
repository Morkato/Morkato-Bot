from discord.embeds import Embed
from typing import Optional

class BaseError(Exception):
  def __init__(self, message: str, action: str, embeds: Optional[list[Embed]]) -> None:
    super().__init__(message, action)

    self.message = message
    self.action = action
    self.embeds = embeds
  
  def __repr__(self) -> str:
    return f'{__name__}.{self.__class__.__name__}({self.message})'

class NotFoundError(BaseError):
  def __init__(self, message: Optional[str] = None, action: Optional[str] = None, embeds: Optional[list[Embed]] = None) -> None:
    message = message or "Não foi possivel achar esse item."
    action = action or "Tente novamente com outro nome."
    embeds = embeds or []

    super().__init__(message, action, embeds)

class AlrearyExistsError(BaseError):
  def __init__(self, message: Optional[str] = None, action: Optional[str] = None, embeds: Optional[list[Embed]] = None) -> None:
    message = message or "Esse item já existe."
    action = action or "Tente novamente com outro nome."
    embeds = embeds or []

    super().__init__(message, action, embeds)

class InternalServerError(BaseError):
  def __init__(self, error: Exception, message: Optional[str] = None, action: Optional[str] = None, embeds: Optional[list[Embed]] = None) -> None:
    message = message or "Erro interno."
    action = action or "Tente novamente com outro nome."
    embeds = embeds or []

    super().__init__(message, action, embeds)

    self.error = error