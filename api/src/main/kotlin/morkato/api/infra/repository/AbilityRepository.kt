package morkato.api.infra.repository

import org.jetbrains.exposed.sql.SqlExpressionBuilder.eq
import org.jetbrains.exposed.sql.deleteWhere
import org.jetbrains.exposed.sql.selectAll
import org.jetbrains.exposed.sql.ResultRow
import org.jetbrains.exposed.sql.update
import org.jetbrains.exposed.sql.insert
import org.jetbrains.exposed.sql.and

import morkato.api.exception.model.AbilityNotFoundError
import morkato.api.infra.tables.abilities
import java.math.BigDecimal
import java.math.RoundingMode

object AbilityRepository {
  public data class AbilityPayload(
    val guildId: String,
    val id: Long,
    val name: String,
    val energy: BigDecimal,
    val percent: BigDecimal,
    val npcType: Int,
    val description: String?,
    val banner: String?
  ) {
    public constructor(row: ResultRow) : this(
      row[abilities.guild_id],
      row[abilities.id],
      row[abilities.name],
      row[abilities.energy],
      row[abilities.percent],
      row[abilities.npc_type],
      row[abilities.description],
      row[abilities.banner]
    ) {}
  }
  private object DefaultValue {
    const val percent: Int = 0
    const val energy: Int = 0
  }
  fun findAllByGuildId(id: String) : Sequence<AbilityPayload> {
    return abilities
      .selectAll()
      .where({
        (abilities.guild_id eq id)
      })
      .asSequence()
      .map(::AbilityPayload)
  }
  fun findById(guildId: String, id: Long) : AbilityPayload {
    return try {
      AbilityPayload(
        abilities
          .selectAll()
          .where({
            (abilities.guild_id eq guildId)
              .and(abilities.id eq id)
          })
          .limit(1)
          .single()
      )
    } catch (exc: NoSuchElementException) {
      val extra: MutableMap<String, Any?> = mutableMapOf()
      extra["guild_id"] = guildId
      extra["id"] = id.toString()
      throw AbilityNotFoundError(extra)
    }
  }
  fun createAbility(
    guildId: String,
    name: String,
    energy: BigDecimal?,
    percent: BigDecimal?,
    npcType: Int,
    description: String?,
    banner: String?
  ) : AbilityPayload {
    val id = abilities.insert {
      it[this.guild_id] = guildId
      it[this.name] = name
      it[this.npc_type] = npcType
      if (energy != null) {
        it[this.energy] = energy
      }
      if (percent != null) {
        it[this.percent] = percent
      }
      if (description != null) {
        it[this.description] = description
      }
      if (banner != null) {
        it[this.banner] = banner
      }
    } get abilities.id
    return AbilityPayload(
      guildId = guildId,
      id = id,
      name = name,
      energy = energy ?: BigDecimal(DefaultValue.energy).setScale(3, RoundingMode.UP),
      percent = percent ?: BigDecimal(0).setScale(3, RoundingMode.UP),
      npcType = npcType,
      description = description,
      banner = banner
    )
  }
  fun updateAbility(
    guildId: String,
    id: Long,
    name: String?,
    energy: BigDecimal?,
    percent: BigDecimal?,
    npcType: Int?,
    description: String?,
    banner: String?
  ) : Unit {
    abilities.update({
      (abilities.guild_id eq guildId)
        .and(abilities.id eq id)
    }) {
      if (name != null) {
        it[this.name] = name
      }
      if (energy != null) {
        it[this.energy] = energy
      }
      if (percent != null) {
        it[this.percent] = percent
      }
      if (npcType != null) {
        it[this.npc_type] = npcType
      }
      if (description != null) {
        it[this.description] = description
      }
      if (banner != null) {
        it[this.banner] = banner
      }
    }
  }
  fun deleteAbility(guildId: String, id: Long) : Unit {
    abilities.deleteWhere {
      (this.guild_id eq guildId)
        .and(this.id eq id)
    }
  }
}