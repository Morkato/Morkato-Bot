package morkato.api.dto.npc

import morkato.api.model.npc.Npc
import morkato.api.model.npc.NpcType
import java.math.BigDecimal
import kotlin.math.round

data class NpcResponseData(
  val guild_id: String,
  val id: String,
  val name: String,
  val type: NpcType,
  val family_id: String,
  val surname: String,
  val max_energy: BigDecimal,
  val energy: BigDecimal,
  val flags: Int,
  val max_life: BigDecimal,
  val max_breath: BigDecimal,
  val max_blood: BigDecimal,
  val current_life: BigDecimal,
  val current_breath: BigDecimal,
  val current_blood: BigDecimal,
  val icon: String?,
  val last_action: Long?,
  val abilities: List<String>,
  val arts: Map<String, BigDecimal>
) {
  public constructor(npc: Npc, abilities: List<String>, arts: Map<String, BigDecimal>) : this(
    npc.guild.id,
    npc.id.toString(),
    npc.name,
    npc.type,
    npc.familyId.toString(),
    npc.surname,
    npc.maxEnergy,
    npc.energy,
    npc.flags,
    npc.maxLife,
    npc.maxBreath,
    npc.maxBlood,
    npc.currentLife,
    npc.currentBreath,
    npc.currentBlood,
    npc.icon,
    npc.lastAction?.toEpochMilli(),
    abilities,
    arts
  );
}
