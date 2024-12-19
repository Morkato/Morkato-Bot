package morkato.api.infra.repository

import morkato.api.exception.model.FamilyNotFoundError
import org.jetbrains.exposed.sql.SqlExpressionBuilder.eq
import org.jetbrains.exposed.sql.deleteWhere
import org.jetbrains.exposed.sql.selectAll
import org.jetbrains.exposed.sql.ResultRow
import org.jetbrains.exposed.sql.update
import org.jetbrains.exposed.sql.insert
import org.jetbrains.exposed.sql.and
import morkato.api.infra.tables.families
import java.math.BigDecimal

object FamilyRepository {
  public data class FamilyPayload(
    val guildId: String,
    val id: Long,
    val name: String,
    val percent: BigDecimal,
    val userType: Int,
    val description: String?,
    val banner: String?
  ) {
    public constructor(row: ResultRow) : this(
      row[families.guild_id],
      row[families.id],
      row[families.name],
      row[families.percent],
      row[families.user_type],
      row[families.description],
      row[families.banner]
    );
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
          .single()
      )
    } catch (exc: NoSuchElementException) {
      throw FamilyNotFoundError(guildId, id.toString())
    }
  }
  fun createFamily(
    guildId: String,
    name: String,
    percent: BigDecimal?,
    userType: Int?,
    description: String?,
    banner: String?
  ) : FamilyPayload {
    val id = families.insert {
      it[this.guild_id] = guildId
      it[this.name] = name
      it[this.description] = description
      it[this.banner] = banner
      if (percent != null) {
        it[this.percent] = percent
      }
      if (userType != null) {
        it[this.user_type] = userType
      }
    } get families.id
    return FamilyPayload(
      guildId = guildId,
      id = id,
      name = name,
      percent = percent ?: BigDecimal(0),
      userType = userType ?: 0,
      description = description,
      banner = banner
    )
  }
  fun updateFamily(
    guildId: String,
    id: Long,
    name: String?,
    percent: BigDecimal?,
    userType: Int?,
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
  fun deleteFamily(guildId: String, id: Long) : Unit {
    families.deleteWhere {
      (this.guild_id eq guildId)
        .and(this.id eq id)
    }
  }
}