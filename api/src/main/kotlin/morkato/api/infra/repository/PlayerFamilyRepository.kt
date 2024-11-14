package morkato.api.infra.repository

import org.jetbrains.exposed.sql.SqlExpressionBuilder.eq
import org.jetbrains.exposed.sql.deleteWhere
import org.jetbrains.exposed.sql.selectAll
import org.jetbrains.exposed.sql.ResultRow
import org.jetbrains.exposed.sql.insert
import org.jetbrains.exposed.sql.and

import morkato.api.infra.tables.players_families

object PlayerFamilyRepository {
  public data class PlayerFamilyPayload(
    val guildId: String,
    val playerId: String,
    val familyId: Long
  ) {
    public constructor(row: ResultRow) : this(
      row[players_families.guild_id],
      row[players_families.player_id],
      row[players_families.family_id]
    );
  }
  fun findAllByGuildIdAndPlayerId(guildId: String, id: String) : Sequence<PlayerFamilyPayload> {
    return players_families
      .selectAll()
      .where({
        (players_families.guild_id eq guildId)
          .and(players_families.player_id eq id)
      })
      .asSequence()
      .map(::PlayerFamilyPayload)
  }
  fun createPlayerFamily(guildId: String, playerId: String, familyId: Long) : PlayerFamilyPayload {
    players_families.insert {
      it[this.guild_id] = guildId
      it[this.player_id] = playerId
      it[this.family_id] = familyId
    }
    return PlayerFamilyPayload(guildId, playerId, familyId)
  }
  fun deletePlayerFamily(guildId: String, playerId: String, familyId: Long) : PlayerFamilyPayload {
    players_families.deleteWhere {
      (this.guild_id eq guildId)
        .and(this.player_id eq playerId)
        .and(this.family_id eq familyId)
    }
    return PlayerFamilyPayload(guildId, playerId, familyId)
  }
}