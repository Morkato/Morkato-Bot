package morkato.api.dto.art

import morkato.api.model.art.ArtType
import morkato.api.model.art.Art
import java.math.BigDecimal

data class ArtResponseData(
  val guild_id: String,
  val id: String,
  val name: String,
  val type: ArtType,
  val description: String?,
  val banner: String?,
  val energy: BigDecimal,
  val life: BigDecimal,
  val breath: BigDecimal,
  val blood: BigDecimal,
  val attacks: List<ArtAttackResponseData>
) {
  public constructor(art: Art, attacks: List<ArtAttackResponseData>) : this(
    art.guild.id,
    art.id.toString(),
    art.name,
    art.type,
    art.description,
    art.banner,
    art.energy,
    art.life,
    art.breath,
    art.blood,
    attacks
  );
}