package morkato.api.dto.guild

import morkato.api.model.guild.Guild
import java.math.BigDecimal

data class GuildResponseData(
  val id: String,
  val human_initial_life: BigDecimal,
  val oni_initial_life: BigDecimal,
  val hybrid_initial_life: BigDecimal,
  val breath_initial: BigDecimal,
  val blood_initial: BigDecimal,
  val family_roll: BigDecimal,
  val ability_roll: BigDecimal,
  val prodigy_roll: BigDecimal,
  val mark_roll: BigDecimal,
  val berserk_roll: BigDecimal,
  val roll_category_id: String?,
  val off_category_id: String?
) {
  public constructor(guild: Guild) : this(
    guild.id,
    guild.humanInitialLife,
    guild.oniInitialLife,
    guild.hybridInitialLife,
    guild.breathInitial,
    guild.bloodInitial,
    guild.familyRoll,
    guild.abilityRoll,
    guild.prodigyRoll,
    guild.markRoll,
    guild.berserkRoll,
    guild.rollCategoryId,
    guild.offCategoryId
  );
}