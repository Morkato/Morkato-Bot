package morkato.api.dto.user

import morkato.api.model.user.UserType
import java.math.BigDecimal

data class UserCreateData(
  val type: UserType,
  val flags: Int?,
  val ability_roll: BigDecimal?,
  val family_roll: BigDecimal?,
  val prodigy_roll: BigDecimal?,
  val mark_roll: BigDecimal?,
  val berserk_roll: BigDecimal?
) {};
