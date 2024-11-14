package morkato.api.dto.guild

import java.time.format.DateTimeFormatter
import morkato.api.model.guild.Guild
import java.math.BigDecimal
import java.time.LocalDateTime
import java.time.ZoneId

data class GuildResponseData(
  val id: String,
  val start_rpg_calendar: String,
  val start_rpg_date: String,
  val human_initial_life: BigDecimal,
  val oni_initial_life: BigDecimal,
  val hybrid_initial_life: BigDecimal,
  val breath_initial: BigDecimal,
  val blood_initial: BigDecimal,
  val family_roll: BigDecimal,
  val ability_roll: BigDecimal,
  val roll_category_id: String?,
  val off_category_id: String?
) {
  companion object {
    val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss'Z'");
  }
  public constructor(guild: Guild) : this(
    guild.id,
    LocalDateTime.ofInstant(guild.startRpgCalendar, ZoneId.systemDefault()).format(formatter),
    LocalDateTime.ofInstant(guild.startRpgDate, ZoneId.systemDefault()).format(formatter),
    guild.humanInitialLife,
    guild.oniInitialLife,
    guild.hybridInitialLife,
    guild.breathInitial,
    guild.bloodInitial,
    guild.familyRoll,
    guild.abilityRoll,
    guild.rollCategoryId,
    guild.offCategoryId
  );
}