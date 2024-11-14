package morkato.api.infra.repository

import org.jetbrains.exposed.sql.SqlExpressionBuilder.eq
import org.jetbrains.exposed.sql.deleteWhere
import org.jetbrains.exposed.sql.selectAll
import org.jetbrains.exposed.sql.ResultRow
import org.jetbrains.exposed.sql.update
import org.jetbrains.exposed.sql.insert
import org.jetbrains.exposed.sql.and

import morkato.api.exception.model.NpcNotFoundError
import morkato.api.infra.tables.npcs
import morkato.api.model.npc.NpcType
import java.math.BigDecimal
import java.math.RoundingMode
import java.time.Instant

object NpcRepository {
  public data class NpcPayload(
    val guildId: String,
    val id: Long,
    val name: String,
    val type: NpcType,
    val familyId: Long,
    val surname: String,
    val maxEnergy: BigDecimal,
    val energy: BigDecimal,
    val flags: Int,
    val maxLife: BigDecimal,
    val maxBreath: BigDecimal,
    val maxBlood: BigDecimal,
    val currentLife: BigDecimal,
    val currentBreath: BigDecimal,
    val currentBlood: BigDecimal,
    val icon: String?,
    val lastAction: Instant?
  ) {
    public constructor(row: ResultRow) : this(
      row[npcs.guild_id],
      row[npcs.id],
      row[npcs.name],
      row[npcs.type],
      row[npcs.family_id],
      row[npcs.surname],
      row[npcs.max_energy],
      row[npcs.energy],
      row[npcs.flags],
      row[npcs.max_life],
      row[npcs.max_breath],
      row[npcs.max_blood],
      row[npcs.current_life],
      row[npcs.current_breath],
      row[npcs.current_blood],
      row[npcs.icon],
      row[npcs.last_action]
    );
  }
  fun findById(guildId: String, id: Long) : NpcPayload {
    return try {
      NpcPayload(
        npcs
          .selectAll()
          .where({
            (npcs.guild_id eq guildId)
              .and(npcs.id eq id)
          })
          .limit(1)
          .single()
      )
    } catch (exc: NoSuchElementException) {
      val extra: MutableMap<String, Any?> = mutableMapOf()
      extra["guild_id"] = guildId
      extra["id"] = id.toString()
      throw NpcNotFoundError(extra)
    }
  }
  fun findBySurname(guildId: String, surname: String) : NpcPayload {
    return try {
      NpcPayload(
        npcs
          .selectAll()
          .where({
            (npcs.guild_id eq guildId)
              .and(npcs.surname eq surname)
          })
          .limit(1)
          .single()
      )
    } catch (exc: NoSuchElementException) {
      val extra: MutableMap<String, Any?> = mutableMapOf()
      extra["guild_id"] = guildId
      extra["id"] = surname
      throw NpcNotFoundError(extra)
    }
  }
  fun findByPlayerId(guildId: String, id: String): NpcPayload {
    return try {
      NpcPayload(
        npcs
          .selectAll()
          .where({
            (npcs.guild_id eq guildId)
              .and(npcs.player_id eq id)
          })
          .limit(1)
          .single()
      )
    } catch (exc: NoSuchElementException) {
      val extra: MutableMap<String, Any?> = mutableMapOf()
      extra["guild_id"] = guildId
      extra["player_id"] = id
      throw NpcNotFoundError(extra)
    }
  }
  fun createNpc(
    playerId: String? = null,
    guildId: String,
    name: String,
    type: NpcType,
    familyId: Long,
    surname: String,
    flags: Int?,
    life: BigDecimal?,
    breath: BigDecimal?,
    blood: BigDecimal?,
    icon: String?
  ) : NpcPayload {
    val result = npcs.insert {
      it[this.guild_id] = guildId
      it[this.name] = name
      it[this.type] = type
      it[this.family_id] = familyId
      it[this.surname] = surname
      it[this.icon] = icon
      if (playerId != null) {
        it[this.player_id] = playerId
      }
      if (flags != null) {
        it[this.flags] = flags
      }
      if (life != null) {
        it[this.max_life] = life
        it[this.current_life] = life
      }
      if (breath != null) {
        it[this.max_breath] = breath
        it[this.current_breath] = breath
      }
      if (blood != null) {
        it[this.max_blood] = blood
        it[this.current_blood] = blood
      }
    }
    val id = result get npcs.id
    val maxEnergy = result get npcs.max_energy
    return NpcPayload(
      guildId = guildId,
      id = id,
      name = name,
      type = type,
      familyId = familyId,
      surname = surname,
      maxEnergy = maxEnergy,
      energy = maxEnergy,
      flags = flags ?: 0,
      maxLife = life ?: BigDecimal(0).setScale(12, RoundingMode.UP),
      maxBreath = breath ?: BigDecimal(0).setScale(12, RoundingMode.UP),
      maxBlood = blood ?: BigDecimal(0).setScale(12, RoundingMode.UP),
      currentLife = life ?: BigDecimal(0).setScale(12, RoundingMode.UP),
      currentBreath = breath ?: BigDecimal(0).setScale(12, RoundingMode.UP),
      currentBlood = blood ?: BigDecimal(0).setScale(12, RoundingMode.UP),
      icon = icon,
      lastAction = null
    )
  }
  fun updateNpc(
    guildId: String,
    id: Long,
    name: String?,
    type: NpcType?,
    surname: String?,
    maxEnergy: BigDecimal?,
    energy: BigDecimal?,
    flags: Int?,
    maxLife: BigDecimal?,
    maxBreath: BigDecimal?,
    maxBlood: BigDecimal?,
    currentLife: BigDecimal?,
    currentBreath: BigDecimal?,
    currentBlood: BigDecimal?,
    icon: String?,
    lastAction: Instant?
  ) : Unit {
    npcs.update({
      (npcs.guild_id eq guildId)
        .and(npcs.id eq id)
    }) {
      if (name != null) {
        it[this.name] = name
      }
      if (type != null) {
        it[this.type] = type
      }
      if (surname != null) {
        it[this.surname] = surname
      }
      if (maxEnergy != null) {
        it[this.max_energy] = maxEnergy
      }
      if (energy != null) {
        it[this.energy] = energy
      }
      if (flags != null) {
        it[this.flags] = flags
      }
      if (maxLife != null) {
        it[this.max_life] = maxLife
      }
      if (maxBreath != null) {
        it[this.max_breath] = maxBreath
      }
      if (maxBlood != null) {
        it[this.max_blood] = maxBlood
      }
      if (currentLife != null) {
        it[this.current_life] = currentLife
      }
      if (currentBreath != null) {
        it[this.current_breath] = currentBreath
      }
      if (currentBlood != null) {
        it[this.current_blood] = currentBlood
      }
      if (icon != null) {
        it[this.icon] = icon
      }
      if (lastAction != null) {
        it[this.last_action] = lastAction
      }
    }
  }
  fun deleteNpc(guildId: String, id: Long) : Unit {
    npcs.deleteWhere {
      (this.guild_id eq guildId)
        .and(this.id eq id)
    }
  }
}