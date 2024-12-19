package morkato.api.dto.family

import morkato.api.dto.validation.DescriptionSchema
import morkato.api.dto.validation.BannerSchema
import morkato.api.dto.validation.NameSchema
import org.jetbrains.annotations.NotNull
import java.math.BigDecimal

data class FamilyCreateData(
  @NameSchema @NotNull val name: String,
  val percent: BigDecimal?,
  val user_type: Int?,
  @DescriptionSchema val description: String?,
  @BannerSchema val banner: String?
) {}
