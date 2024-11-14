package morkato.api.dto.npc

import jakarta.validation.constraints.Digits
import morkato.api.dto.validation.BannerSchema
import morkato.api.dto.validation.NameSchema
import morkato.api.dto.validation.AttrSchema
import morkato.api.dto.validation.KeySchema
import morkato.api.model.npc.NpcType
import java.math.BigDecimal

data class NpcUpdateData(
  @NameSchema val name: String?,
  @KeySchema val surname: String?,
  val type: NpcType?,
  @Digits(integer = 3, fraction = 0)
  val energy: BigDecimal?,
  val flags: Int?,
  @AttrSchema val max_life: BigDecimal?,
  @AttrSchema val max_breath: BigDecimal?,
  @AttrSchema val max_blood: BigDecimal?,
  @AttrSchema val current_life: BigDecimal?,
  @AttrSchema val current_breath: BigDecimal?,
  @AttrSchema val current_blood: BigDecimal?,
  @BannerSchema val icon: String?,
  val last_action: Long?
);