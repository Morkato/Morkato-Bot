package morkato.api.infra.repository

import org.jetbrains.exposed.sql.SqlExpressionBuilder.eq
import org.jetbrains.exposed.sql.deleteWhere
import org.jetbrains.exposed.sql.selectAll
import org.jetbrains.exposed.sql.ResultRow
import org.jetbrains.exposed.sql.update
import org.jetbrains.exposed.sql.insert
import org.jetbrains.exposed.sql.and

import morkato.api.infra.tables.npcs_abilities

object NpcAbilityRepository {
  public data class NpcAbilityPayload(
    val guildId: String,
    val npcId: Long,
    val abilityId: Long
  ) {
    public constructor(row: ResultRow) : this(
      row[npcs_abilities.guild_id],
      row[npcs_abilities.npc_id],
      row[npcs_abilities.ability_id]
    );
  }
  fun findAllByGuildIdAndNpcId(guildId: String, npcId: Long) : Sequence<NpcAbilityPayload> {
    return npcs_abilities
      .selectAll()
      .where({
        (npcs_abilities.guild_id eq guildId)
          .and(npcs_abilities.npc_id eq npcId)
      })
      .asSequence()
      .map(::NpcAbilityPayload)
  }
  fun createNpcAbility(guildId: String, npcId: Long, abilityId: Long) : NpcAbilityPayload {
    npcs_abilities.insert {
      it[this.guild_id] = guildId
      it[this.npc_id] = npcId
      it[this.ability_id] = abilityId
    }
    return NpcAbilityPayload(
      guildId = guildId,
      npcId = npcId,
      abilityId = abilityId
    )
  }
}