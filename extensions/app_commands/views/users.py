from typing import Literal

from discord import app_commands, ui

from morkato import (
  utils
)

MEMBERS_TYPE = Literal[1, 2, 3]
member_choice = [
  app_commands.Choice(name="Apenas Membros", value=1),
  app_commands.Choice(name="Apenas Bots", value=2),
  app_commands.Choice(name="Membros e Bots", value=3)
]