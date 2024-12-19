package morkato.api.dto.family

import morkato.api.model.family.Family
import java.math.BigDecimal

data class FamilyResponseData(
  val guild_id: String,
  val id: String,
  val name: String,
  val percent: BigDecimal,
  val user_type: Int,
  val description: String?,
  val banner: String?
) {
  public constructor(family: Family) : this(
    family.guild.id,
    family.id.toString(),
    family.name,
    family.percent,
    family.userType,
    family.description,
    family.banner
  );
}