from morkato.work.builder import (
  UnknownMessageContent,
  MessageBuilder
)
from morkato.family import Family
from morkato.player import Player

class AppError(Exception):
  def __init__(self, key: str, /, *args, **parameters) -> None:
    self.key = key
    self.args = args
    self.parameters = parameters
  def build(self, builder: MessageBuilder, lang: str, /) -> str:
    try:
      return builder.get_content(lang, self.key, *self.args, **self.parameters)
    except UnknownMessageContent:
      return "Unknown message content for key: **`%s.%s`**" % (lang, self.key)
class ArtNotFoundError(AppError):
  def __init__(self, art_query: str) -> None:
    super().__init__(f"error{type(self).__name__}", art_query)
class AttackNotFoundError(AppError):
  def __init__(self, attack_query: str) -> None:
    super().__init__(f"error{type(self).__name__}", attack_query)
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