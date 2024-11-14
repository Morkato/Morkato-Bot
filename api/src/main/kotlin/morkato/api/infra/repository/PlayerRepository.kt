package morkato.api.infra.repository

import org.jetbrains.exposed.sql.SqlExpressionBuilder.eq
import org.jetbrains.exposed.sql.deleteWhere
import org.jetbrains.exposed.sql.selectAll
import org.jetbrains.exposed.sql.ResultRow
import org.jetbrains.exposed.sql.update
import org.jetbrains.exposed.sql.insert
import org.jetbrains.exposed.sql.and

import morkato.api.exception.model.PlayerNotFoundError
import morkato.api.infra.tables.players
import morkato.api.model.npc.NpcType
import java.math.BigDecimal
import java.math.RoundingMode

object PlayerRepository {
  public data class PlayerPayload(
    val guildId: String,
    val id: String,
    val npcType: NpcType,
    val familyId: Long?,
    val abilityRoll: BigDecimal,
    val familyRoll: BigDecimal,
    val prodigyRoll: BigDecimal,
    val markRoll: BigDecimal,
    val berserkRoll: BigDecimal,
    val flags: Int
  ) {
    public constructor(row: ResultRow) : this(
      row[players.guild_id],
      row[players.id],
      row[players.npc_type],
      row[players.family_id],
      row[players.ability_roll],
      row[players.family_roll],
      row[players.prodigy_roll],
      row[players.mark_roll],
      row[players.berserk_roll],
      row[players.flags]
    );
  }
  fun findById(guildId: String, id: String) : PlayerPayload {
    return try {
      PlayerPayload(
        players
          .selectAll()
          .where({
            (players.guild_id eq guildId)
              .and(players.id eq id)
          })
          .limit(1)
          .single()
      )
    } catch (exc: NoSuchElementException) {
      val extra: MutableMap<String, Any?> = mutableMapOf()
      extra["guild_id"] = guildId
      extra["id"] = id
      throw PlayerNotFoundError(extra)
    }
  }
  fun createPlayer(
    guildId: String,
    id: String,
    npcType: NpcType,
    familyId: Long?,
    abilityRoll: BigDecimal?,
    familyRoll: BigDecimal?,
    prodigyRoll: BigDecimal?,
    markRoll: BigDecimal?,
    berserkRoll: BigDecimal?,
    flags: Int?
  ) : PlayerPayload {
    players.insert {
      it[this.guild_id] = guildId
      it[this.id] = id
      it[this.npc_type] = npcType
      it[this.family_id] = familyId
      if (abilityRoll != null) {
        it[this.ability_roll] = abilityRoll
      }
      if (familyRoll != null) {
        it[this.family_roll] = familyRoll
      }
      if (prodigyRoll != null) {
        it[this.prodigy_roll] = prodigyRoll
      }
      if (markRoll != null) {
        it[this.mark_roll] = markRoll
      }
      if (berserkRoll != null) {
        it[this.berserk_roll] = berserkRoll
      }
      if (flags != null) {
        it[this.flags] = flags
      }
    }
    return PlayerPayload(
      guildId = guildId,
      id = id,
      npcType = npcType,
      familyId = familyId,
      abilityRoll = abilityRoll ?: BigDecimal(3).setScale(3, RoundingMode.UP),
      familyRoll = familyRoll ?: BigDecimal(3).setScale(3, RoundingMode.UP),
      prodigyRoll = prodigyRoll ?: BigDecimal(1).setScale(3, RoundingMode.UP),
      markRoll = markRoll ?: BigDecimal(1).setScale(3, RoundingMode.UP),
      berserkRoll = berserkRoll ?: BigDecimal(1).setScale(3, RoundingMode.UP),
      flags = flags ?: 0
    )
  }
  fun updatePlayer(
    guildId: String,
    id: String,
    familyId: Long?,
    abilityRoll: BigDecimal?,
    familyRoll: BigDecimal?,
    prodigyRoll: BigDecimal?,
    markRoll: BigDecimal?,
    berserkRoll: BigDecimal?,
    flags: Int?,
  ) : Unit {
    players.update({
      (players.guild_id eq guildId)
        .and(players.id eq id)
    }) {
      if (familyId != null) {
        it[this.family_id] = familyId
      }
      if (abilityRoll != null) {
        it[this.ability_roll] = abilityRoll
      }
      if (familyRoll != null) {
        it[this.family_roll] = familyRoll
      }
      if (prodigyRoll != null) {
        it[this.prodigy_roll] = prodigyRoll
      }
      if (markRoll != null) {
        it[this.mark_roll] = markRoll
      }
      if (berserkRoll != null) {
        it[this.berserk_roll] = berserkRoll
      }
      if (flags != null) {
        it[this.flags] = flags
      }
    }
  }
  fun deletePlayer(guildId: String, id: String) : Unit {
    players.deleteWhere {
      (this.guild_id eq guildId)
        .and(this.id eq id)
    }
  }
}