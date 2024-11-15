from morkato.work.builder import (
  UnknownMessageContent,
  MessageBuilder
)
from morkato.attack import Attack
from morkato.family import Family
from morkato.player import Player
from typing_extensions import Self

class NoActionError(Exception): ...
class AppError(Exception):
  def __init__(self, key: str, /, *args, **parameters) -> None:
    self.key = key
    self.args = args
    self.parameters = parameters
    self.reply_message = False
    self.is_unknown_params = False
  def reply(self) -> Self:
    self.reply_message = True
    return self
  def unkown_params(self) -> Self:
    self.is_unknown_params = True
    return self
  def build(self, builder: MessageBuilder, lang: str, /) -> str:
    try:
      return builder.get_content(lang, self.key, *self.args, **self.parameters)
    except UnknownMessageContent:
      return "Unknown message content for key: **`%s.%s`**" % (lang, self.key)
class ValidationError(AppError): ...
class ArtNotFoundError(AppError):
  def __init__(self, art_query: str) -> None:
    super().__init__(f"error{type(self).__name__}", art_query)
class AttackNotFoundError(AppError):
  def __init__(self, attack_query: str) -> None:
    super().__init__(f"error{type(self).__name__}", attack_query)
class ManyAttackError(AppError):
  def __init__(self, attack: Attack) -> None:
    super().__init__(f"error{type(self).__name__}", attack.name)
    self.attack = attack
class AbilityNotFoundError(AppError):
  def __init__(self, ability_query: str) -> None:
    super().__init__(f"error{type(self).__name__}", ability_query)
class FamilyNotFoundError(AppError):
  def __init__(self, family_query: str) -> None:
    super().__init__(f"error{type(self).__name__}", family_query)
class PlayerAlreadyRegisteredFamily(AppError):
  def __init__(self, player: Player) -> None:
    super().__init__(f"error{type(self).__name__}")
    self.player = player
class DoNotPlayerHasFamily(AppError):
  def __init__(self, player: Player, family: Family) -> None:
    super().__init__(f"error{type(self).__name__}", family.name)
    self.player = player
    self.family = family
class PlayerHasFamilyRolls(AppError):
  def __init__(self, player: Player) -> None:
    super().__init__(f"error{type(self).__name__}", player.family_roll)
    self.player = player