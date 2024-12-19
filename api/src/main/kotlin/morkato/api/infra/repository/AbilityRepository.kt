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

object AbilityRepository {
  public data class AbilityPayload(
    val guildId: String,
    val id: Long,
    val name: String,
    val percent: BigDecimal,
    val userType: Int,
    val description: String?,
    val banner: String?
  ) {
    public constructor(row: ResultRow) : this(
      row[abilities.guild_id],
      row[abilities.id],
      row[abilities.name],
      row[abilities.percent],
      row[abilities.user_type],
      row[abilities.description],
      row[abilities.banner]
    );
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
      throw AbilityNotFoundError(guildId, id.toString())
    }
  }
  fun createAbility(
    guildId: String,
    name: String,
    userType: Int?,
    percent: BigDecimal?,
    description: String?,
    banner: String?
  ) : AbilityPayload {
    val id = abilities.insert {
      it[this.guild_id] = guildId
      it[this.name] = name
      it[this.description] = description
      it[this.banner] = banner
      if (userType != null) {
        it[this.user_type] = userType
      }
      if (percent != null) {
        it[this.percent] = percent
      }
    } get abilities.id
    return AbilityPayload(
      guildId = guildId,
      id = id,
      name = name,
      percent = percent ?: BigDecimal(0),
      userType = userType ?: 0,
      description = description,
      banner = banner
    )
  }
  fun updateAbility(
    guildId: String,
    id: Long,
    name: String?,
    userType: Int?,
    percent: BigDecimal?,
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
      if (userType != null) {
        it[this.user_type] = userType
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
  fun deleteAbility(guildId: String, id: Long) : Unit {
    abilities.deleteWhere {
      (this.guild_id eq guildId)
        .and(this.id eq id)
    }
  }
}