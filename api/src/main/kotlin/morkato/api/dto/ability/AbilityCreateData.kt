package morkato.api.dto.ability

import jakarta.validation.constraints.Digits
import jakarta.validation.constraints.NotNull
import morkato.api.dto.validation.AttrSchema
import morkato.api.dto.validation.DescriptionSchema
import morkato.api.dto.validation.BannerSchema
import morkato.api.dto.validation.NameSchema
import morkato.api.model.ability.AbilityType
import java.math.BigDecimal

data class AbilityCreateData(
  @NameSchema @NotNull val name: String,
  @Digits(integer = 3, fraction = 0)
  val energy: BigDecimal?,
  val percent: BigDecimal?,
  @NotNull val npc_type: Int,
  @DescriptionSchema val description: String?,
  @BannerSchema val banner: String?
) {}