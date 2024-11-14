package morkato.api.dto.art

import jakarta.validation.constraints.Digits
import morkato.api.dto.validation.DescriptionSchema
import morkato.api.dto.validation.BannerSchema
import morkato.api.dto.validation.NameSchema
import morkato.api.dto.validation.AttrSchema
import morkato.api.model.art.ArtType
import java.math.BigDecimal

data class ArtUpdateData(
  @NameSchema val name: String?,
  val type: ArtType?,
  @DescriptionSchema val description: String?,
  @BannerSchema val banner: String?,
  @Digits(integer = 3, fraction = 0)
  val energy: BigDecimal?,
  @AttrSchema val life: BigDecimal?,
  @AttrSchema val breath: BigDecimal?,
  @AttrSchema val blood: BigDecimal?
) {}
