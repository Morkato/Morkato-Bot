package morkato.api.dto.player

import jakarta.validation.constraints.Digits
import java.math.BigDecimal

data class PlayerUpdateData(
  val family_id: String?,
  @Digits(integer = 3, fraction = 0)
  val ability_roll: BigDecimal?,
  @Digits(integer = 3, fraction = 0)
  val family_roll: BigDecimal?,
  @Digits(integer = 3, fraction = 0)
  val prodigy_roll: BigDecimal?,
  @Digits(integer = 3, fraction = 0)
  val mark_roll: BigDecimal?,
  @Digits(integer = 3, fraction = 0)
  val berserk_roll: BigDecimal?,
  val flags: Int?
);