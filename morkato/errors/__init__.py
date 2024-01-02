from __future__ import annotations

from typing_extensions import Self
from typing import (
  TYPE_CHECKING,
  Optional,
  ClassVar,
  Tuple,
  Type,
  Dict,
  Any
)

if TYPE_CHECKING:
  from ..context import MorkatoContext

from enum import Enum

class ErrorType(Enum):
  GENERIC = 'generic.unknown'
  GENERIC_NOTFOUND = 'generic.notfound'
  GENERIC_ALREADYEXISTS = 'generic.alreadyexists'

  GUILD_NOTFOUND = 'guild.notfound'
  GUILD_ALREADYEXISTS = 'guild.alreadyexists'

  ART_NOTFOUND = 'art.notfound'
  ART_ALREADYEXISTS = 'art.alreadyexists'

  ATTACK_NOTFOUND = 'attack.notfound'
  ATTACK_ALREADYEXISTS = 'attack.alreadyexists'

  ITEM_NOTFOUND = 'item.notfound'
  ITEM_ALREADYEXISTS = 'item.alreadyexists'

  PLAYER_NOTFOUND = 'player.notfound'
  PLAYER_ALREADYEXISTS = 'player.alreadyexists'

  def __repr__(self) -> str:
    return repr(self.value)
  
  def __str__(self) -> str:
    return str(self.value)
  
  def __hash__(self) -> int:
    return hash(self.value)

  def __eq__(self, other: Any) -> bool:
    return self.value == other

def geterr(type: Optional[ErrorType] = None, *, message: Optional[str] = None, messages: Optional[Dict[str, str]] = None) -> BaseError:
  cls: Type[BaseError] = BaseError

  if not type:
    return cls(message, messages=messages)

  if type in (
    ErrorType.GENERIC_NOTFOUND,
    ErrorType.GUILD_NOTFOUND,
    ErrorType.ART_NOTFOUND,
    ErrorType.ATTACK_NOTFOUND,
    ErrorType.ITEM_NOTFOUND,
    ErrorType.PLAYER_NOTFOUND
  ):
    cls = NotFoundError
  
  elif type in (
    ErrorType.GENERIC_ALREADYEXISTS,
    ErrorType.GUILD_ALREADYEXISTS,
    ErrorType.ART_ALREADYEXISTS,
    ErrorType.ATTACK_ALREADYEXISTS,
    ErrorType.ITEM_ALREADYEXISTS,
    ErrorType.PLAYER_ALREADYEXISTS
  ):
    cls = AlreadyExistsError

  return cls(message, type, messages=messages)

class BaseErrorMeta(type):
  DEFAULT_MESSAGE: ClassVar[str] = "Erro interno, desculpe-me."
  DEFAULT_TYPE: ClassVar[ErrorType] = ErrorType.GENERIC
  DEFAULT_MESSAGES: ClassVar[Dict[str, str]] = {
    ErrorType.GUILD_NOTFOUND: "Esse servidor requer configuração.",
    ErrorType.ART_NOTFOUND: "Essa arte (Respiração, Kekkijutsu ou Estilo de Luta) não existe.",
    ErrorType.ATTACK_NOTFOUND: "Esse ataque não existe.",
    ErrorType.ITEM_NOTFOUND: "Esse item não existe.",
    ErrorType.PLAYER_NOTFOUND: "Esse player não existe.",

    ErrorType.GUILD_ALREADYEXISTS: "Esse servidor já está configurado.",
    ErrorType.ART_ALREADYEXISTS: "Essa arte (Respiração, Kekkijutsu ou Estilo de Luta) já existe.",
    ErrorType.ATTACK_ALREADYEXISTS: "Esse ataque já existe.",
    ErrorType.ITEM_ALREADYEXISTS: "Esse item já existe.",
    ErrorType.PLAYER_ALREADYEXISTS: "Esse player já existe.",
  }
  
  def __new__(cls, name: str, bases: Tuple[Type[Any]], attrs: Dict[str, Any], /, **kwargs) -> Self:
    message = kwargs.pop('message', "Erro interno, desculpe-me.")
    type = kwargs.pop('type', ErrorType.GENERIC)

    if not isinstance(type, ErrorType):
      type = ErrorType.GENERIC

    for (key, value) in attrs.items():
      if key == 'DEFAULT_MESSAGES':
        if not isinstance(value, dict):
          value = dict()
        
        value.update(BaseErrorMeta.DEFAULT_MESSAGES)
        attrs[key] = value
        
        break
    
    message = message if isinstance(message, str) else str(message)

    attrs['DEFAULT_MESSAGE'] = message
    attrs['DEFAULT_TYPE'] = type

    return super().__new__(cls, name, bases, attrs, **kwargs)

class BaseError(Exception, metaclass=BaseErrorMeta):
  def __init__(
    self,
    message:  Optional[str]            = None,
    type:     Optional[ErrorType]      = None, *,
    messages: Optional[Dict[str, str]] = None
  ) -> None:
    super().__init__()

    cls = self.__class__

    type = type or cls.DEFAULT_TYPE

    if messages is None:
      messages = {  }
    
    messages.update(cls.DEFAULT_MESSAGES)
    
    self.message = message or messages.get(type, cls.DEFAULT_MESSAGE)
    self.type = type
  
  def get_logging_error(self) -> str:
    return '[%s: %s] %s' % (
      self.__class__.__name__,
      self.type,
      self.message
    )
  
  def get_discord_message(self) -> str:
    return "**`%s`**" % self.get_logging_error()

class MessageErrorDiscordLogging(BaseError):
  def get_discord_message(self) -> str:
    return self.message

class NotFoundError(MessageErrorDiscordLogging, message="Não foi possível encontrar esse item.", type=ErrorType.GENERIC_NOTFOUND): ...
class ExcludedError(MessageErrorDiscordLogging, message="Esse item existe, porém foi desativado.", type=ErrorType.GENERIC): ...
class AlreadyExistsError(MessageErrorDiscordLogging, message="Esse item já existe.", type=ErrorType.GENERIC_ALREADYEXISTS): ...
class InternalError(MessageErrorDiscordLogging, message="Erro interno, desculpe-me", type=ErrorType.GENERIC): ...
class InternalServerError(MessageErrorDiscordLogging, message="Um erro interno em minha API, desculpe-me.", type=ErrorType.GENERIC): ...
class ValidationError(MessageErrorDiscordLogging, message="Erro de validação, isso acontece quando um dado invalido está sendo enviado.", type=ErrorType.GENERIC): ...