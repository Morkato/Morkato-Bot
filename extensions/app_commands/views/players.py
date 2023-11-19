from discord import app_commands, ui

from morkato import (
  utils
)

breed = [
  app_commands.Choice(name="Humano", value="HUMAN"),
  app_commands.Choice(name="Oni", value="ONI"),
  app_commands.Choice(name="Híbrido", value="HYBRID")
]