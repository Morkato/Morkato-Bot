package morkato.api.dto.ability

import morkato.api.model.ability.Ability
import morkato.api.model.ability.AbilityType
import java.math.BigDecimal

data class AbilityResponseData(
  val guild_id: String,
  val id: String,
  val name: String,
  val energy: BigDecimal,
  val percent: BigDecimal,
  val npc_type: Int,
  val description: String?,
  val banner: String?
) {
  public constructor(ability: Ability) : this(
    ability.guild.id,
    ability.id.toString(),
    ability.name,
    ability.energy,
    ability.percent,
    ability.npcType,
    ability.description,
    ability.banner
  );
}
