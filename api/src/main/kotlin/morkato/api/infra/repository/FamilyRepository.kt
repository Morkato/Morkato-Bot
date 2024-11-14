package morkato.api.infra.repository

import org.jetbrains.exposed.sql.SqlExpressionBuilder.eq
import org.jetbrains.exposed.sql.deleteWhere
import org.jetbrains.exposed.sql.selectAll
import org.jetbrains.exposed.sql.ResultRow
import org.jetbrains.exposed.sql.update
import org.jetbrains.exposed.sql.insert
import org.jetbrains.exposed.sql.and

import morkato.api.exception.model.FamilyNotFoundError
import morkato.api.infra.tables.families
import morkato.api.model.npc.NpcType
import java.math.BigDecimal
import java.math.RoundingMode

object FamilyRepository {
  public data class FamilyPayload(
    val guildId: String,
    val id: Long,
    val percent: BigDecimal,
    val npcType: Int,
    val name: String,
    val description: String?,
    val banner: String?
  ) {
    public constructor(row: ResultRow) : this(
      row[families.guild_id],
      row[families.id],
      row[families.percent],
      row[families.npc_type],
      row[families.name],
      row[families.description],
      row[families.banner]
    ) {}
  }
  fun findAllByGuildId(id: String) : Sequence<FamilyPayload> {
    return families
      .selectAll()
      .where({
        (families.guild_id eq id)
      })
      .asSequence()
      .map(::FamilyPayload)
  }
  fun findById(guildId: String, id: Long) : FamilyPayload {
    return try {
      FamilyPayload(
        families
          .selectAll()
          .where({
            (families.guild_id eq guildId)
              .and(families.id eq id)
          })
          .limit(1)
          .single()
      )
    } catch (exc: NoSuchElementException) {
      val extra: MutableMap<String, Any?> = mutableMapOf()
      extra["guild_id"] = guildId
      extra["id"] = id.toString()
      throw FamilyNotFoundError(extra)
    }
  }
  fun createFamily(
    guildId: String,
    name: String,
    npcType: Int?,
    percent: BigDecimal?,
    description: String?,
    banner: String?
  ) : FamilyPayload {
    val id = families.insert {
      it[this.guild_id] = guildId
      it[this.name] = name
      it[this.npc_type] = npcType ?: 0
      it[this.description] = description
      it[this.banner] = banner
      if (percent != null) {
        it[this.percent] = percent
      }
    } get families.id
    return FamilyPayload(
      guildId = guildId,
      id = id,
      name = name,
      npcType = npcType ?: 0,
      percent = percent ?: BigDecimal(0).setScale(3, RoundingMode.UP),
      description = description,
      banner = banner
    )
  }
  fun updateFamily(
    guildId: String,
    id: Long,
    name: String?,
    npcType: Int?,
    percent: BigDecimal?,
    description: String?,
    banner: String?
  ) : Unit {
    families.update({
      (families.guild_id eq guildId)
        .and(families.id eq id)
    }) {
      if (name != null) {
        it[this.name] = name
      }
      if (npcType != null) {
        it[this.npc_type] = npcType
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
    }
  }
  fun deleteFamily(guildId: String, id: Long) : Unit {
    families.deleteWhere {
      (this.guild_id eq guildId)
        .and(this.id eq id)
    }
  }
}