package morkato.api.dto.player

import jakarta.validation.constraints.Digits
import morkato.api.dto.validation.AttrSchema
import morkato.api.model.npc.NpcType
import java.math.BigDecimal

data class PlayerCreateData(
  val npc_type: NpcType,
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
