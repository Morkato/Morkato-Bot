from __future__ import annotations

from typing import (
  TYPE_CHECKING,
  List
)

if TYPE_CHECKING:
  from ..attack import ItemAttack

from . import ErrorType, BaseError
from random import choice

class ManyItemAttackError(BaseError, message="Existem outros ataques com esse mesmo nome, tente especificar um item.", type=ErrorType.GENERIC):
  def __init__(self, attacks: List[ItemAttack]) -> None:
    super().__init__()

    self.attacks = attacks
  
  def get_discord_message(self) -> str:
    attack = choice(self.attacks)

    item_name = attack.item.name
    attack_name = attack.name

    return "Existem outros ataques com esse mesmo nome, tente especificar o item, por exemplo: **`%s: %s`**" % (
      item_name,
      attack_name
    )