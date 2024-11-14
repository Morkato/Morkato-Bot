package morkato.api.dto.guild

import com.fasterxml.jackson.annotation.JsonFormat
import jakarta.validation.constraints.Digits
import jakarta.validation.constraints.NotNull
import morkato.api.dto.validation.AttrSchema
import java.math.BigDecimal
import java.time.Instant

data class GuildCreateData(
  @NotNull
  val start_rpg_calendar: Instant,
  val start_rpg_date: Instant?,
  @AttrSchema val human_initial_life: BigDecimal?,
  @AttrSchema val oni_initial_life: BigDecimal?,
  @AttrSchema val hybrid_initial_life: BigDecimal?,
  @AttrSchema val breath_initial: BigDecimal?,
  @AttrSchema val blood_initial: BigDecimal?,
  @Digits(integer = 3, fraction = 0)
  val family_roll: BigDecimal?,
  @Digits(integer = 3, fraction = 0)
  val ability_roll: BigDecimal?,
  val roll_category_id: String?,
  val off_category_id: String?
)
