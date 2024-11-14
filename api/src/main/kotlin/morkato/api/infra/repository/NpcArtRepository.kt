package morkato.api.infra.repository

import org.jetbrains.exposed.exceptions.ExposedSQLException
import org.jetbrains.exposed.sql.SqlExpressionBuilder.eq
import org.jetbrains.exposed.sql.SqlExpressionBuilder
import org.jetbrains.exposed.sql.deleteWhere
import org.jetbrains.exposed.sql.selectAll
import org.jetbrains.exposed.sql.ResultRow
import org.jetbrains.exposed.sql.update
import org.jetbrains.exposed.sql.insert
import org.jetbrains.exposed.sql.and
import java.sql.SQLIntegrityConstraintViolationException

import morkato.api.infra.tables.npcs_arts
import java.math.BigDecimal

object NpcArtRepository {
  public data class NpcArtPayload(
    val guildId: String,
    val npcId: Long,
    val artId: Long,
    val exp: BigDecimal
  ) {
    public constructor(row: ResultRow) : this(
      row[npcs_arts.guild_id],
      row[npcs_arts.npc_id],
      row[npcs_arts.art_id],
      row[npcs_arts.exp]
    );
  }
  fun getAllByGuildIdAndNpcId(guildId: String, id: Long): Sequence<NpcArtPayload> {
    return npcs_arts
      .selectAll()
      .where({
        (npcs_arts.guild_id eq guildId)
          .and(npcs_arts.npc_id eq id)
      })
      .map(::NpcArtPayload)
      .asSequence()
  }
  fun createOrUpdateNpcArt(
    guildId: String,
    npcId: Long,
    artId: Long,
    exp: BigDecimal
  ) : NpcArtPayload {
    return try {
      this.createNpcArt(guildId, npcId, artId, exp)
    } catch (exc: ExposedSQLException) {
      this.updateNpcArt(guildId, npcId, artId, exp)
      NpcArtPayload(guildId, npcId, artId, exp)
    }
  }
  fun createNpcArt(
    guildId: String,
    npcId: Long,
    artId: Long,
    exp: BigDecimal
  ) : NpcArtPayload {
    npcs_arts.insert {
      it[this.guild_id] = guildId
      it[this.npc_id] = npcId
      it[this.art_id] = artId
      it[this.exp] = exp
    }
    return NpcArtPayload(
      guildId = guildId,
      npcId = npcId,
      artId = artId,
      exp = exp
    )
  }
  fun updateNpcArt(
    guildId: String,
    npcId: Long,
    artId: Long,
    exp: BigDecimal
  ) : Unit {
    npcs_arts.update({
      (npcs_arts.guild_id eq guildId)
        .and(npcs_arts.npc_id eq npcId)
        .and(npcs_arts.art_id eq artId)
    }) {
      it[this.exp] = exp
    }
  }
  fun deleteNpcArt(
    guildId: String,
    npcId: Long,
    artId: Long
  ) : Unit {
    npcs_arts.deleteWhere {
      (this.guild_id eq guildId)
        .and(this.npc_id eq npcId)
        .and(this.art_id eq artId)
    }
  }
}