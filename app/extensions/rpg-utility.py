from morkato.work.builder import MessageBuilder
from morkato.work.project import registry
from morkato.types import (AbilityType, NpcType, ArtType)
from morkato.errors import PlayerNotFoundError
from morkato.attack import AttackIntents
from discord.interactions import Interaction
from discord import app_commands as apc
from discord.user import User
from app.extension import BaseExtension
from typing import (
  Optional,
  ClassVar,
  Dict
)
import app.checks
import app.utils

has_guild_perms = app.checks.has_guild_permissions(manage_guild=True)

@registry
class RPGUtility(BaseExtension):
  pass