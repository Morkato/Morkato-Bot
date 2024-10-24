from morkato.work.extension import (command)
from morkato.work.project import registry
from app.extension import BaseExtension
from discord.interactions import Interaction
from discord import app_commands as apc
from datetime import datetime
from typing import Optional
import app.converters
import app.errors
import app.checks

@registry
class RPGGuild(BaseExtension):
  LANGUAGE: str
  async def setup(self) -> None:
    self.has_guild_perms = app.checks.has_guild_permissions(manage_guild=True)
    self.LANGUAGE = self.builder.PT_BR
  @apc.command(
    name = "guild-registry",
    description = "[RPG Utilitários] Registra as configurações de uma guilda."
  )
  @apc.guild_only()
  async def guild_registry(
    self, interaction: Interaction, *,
    start_rpg_calendar: str,
    start_rpg_date: Optional[str],
    human_initial_life: Optional[int],
    oni_initial_life: Optional[int],
    hybrid_initial_life: Optional[int],
    breath_initial: Optional[int],
    blood_initial: Optional[int],
    family_roll: Optional[int],
    ability_roll: Optional[int],
    roll_category_id: Optional[str],
    off_category_id: Optional[str]
  ) -> None:
    await interaction.response.defer()
    await self.connection.create_guild(
      id = interaction.guild.id,
      start_rpg_calendar = start_rpg_calendar,
      start_rpg_date = start_rpg_date,
      human_initial_life = human_initial_life,
      oni_initial_life = oni_initial_life,
      hybrid_initial_life = hybrid_initial_life,
      breath_initial = breath_initial,
      blood_initial = blood_initial,
      family_roll = family_roll,
      ability_roll = ability_roll,
      roll_category_id = roll_category_id,
      off_category_id = off_category_id
    )
    content = self.get_content(self.LANGUAGE, "onGuildRegistry")
    await interaction.edit_original_response(content=content)