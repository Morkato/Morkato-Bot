package morkato.api.dto.ability

import morkato.api.model.ability.Ability
import java.math.BigDecimal

data class AbilityResponseData(
  val guild_id: String,
  val id: String,
  val name: String,
  val percent: BigDecimal,
  val user_type: Int,
  val description: String?,
  val banner: String?
) {
  public constructor(ability: Ability) : this(
    ability.guild.id,
    ability.id.toString(),
    ability.name,
    ability.percent,
    ability.userType,
    ability.description,
    ability.banner
  );
}