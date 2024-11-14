package morkato.api.dto.player

import morkato.api.dto.npc.NpcResponseData
import morkato.api.infra.repository.NpcAbilityRepository
import morkato.api.model.npc.Npc
import morkato.api.model.npc.NpcType
import morkato.api.model.player.Player
import java.math.BigDecimal

data class PlayerResponseData(
  val guild_id: String,
  val id: String,
  val npc_type: NpcType,
  val family_id: String?,
  val ability_roll: BigDecimal,
  val family_roll: BigDecimal,
  val prodigy_roll: BigDecimal,
  val mark_roll: BigDecimal,
  val berserk_roll: BigDecimal,
  val flags: Int,
  val abilities: List<String>,
  val families: List<String>,
  val npc: NpcResponseData?
) {
  public constructor(player: Player, abilities: List<String>, families: List<String>, npc: Npc?) : this(
    player.guild.id,
    player.id,
    player.npcType,
    player.familyId?.toString(),
    player.abilityRoll,
    player.familyRoll,
    player.prodigyRoll,
    player.markRoll,
    player.berserkRoll,
    player.flags,
    abilities,
    families,
    if (npc != null) NpcResponseData(
      npc,
      npc.getAllAbilities()
        .map(NpcAbilityRepository.NpcAbilityPayload::abilityId)
        .map(Long::toString)
        .toList(),
      npc.getAllArts()
        .map { it.artId.toString() to it.exp }
        .toMap()
    ) else null
  );
}