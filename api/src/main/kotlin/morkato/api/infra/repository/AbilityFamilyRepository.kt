package morkato.api.infra.repository

import org.jetbrains.exposed.sql.SqlExpressionBuilder.eq
import org.jetbrains.exposed.sql.deleteWhere
import org.jetbrains.exposed.sql.selectAll
import org.jetbrains.exposed.sql.ResultRow
import org.jetbrains.exposed.sql.update
import org.jetbrains.exposed.sql.insert
import org.jetbrains.exposed.sql.and

import morkato.api.infra.tables.abilities_families

object AbilityFamilyRepository {
  public data class AbilityFamilyPayload(
    val guildId: String,
    val abilityId: Long,
    val familyId: Long
  ) {
    public constructor(row: ResultRow) : this(
      row[abilities_families.guild_id],
      row[abilities_families.ability_id],
      row[abilities_families.family_id]
    );
  }
  fun findAllByGuildId(id: String) : Sequence<AbilityFamilyPayload> {
    return abilities_families
      .selectAll()
      .where({
        (abilities_families.guild_id eq id)
      })
      .asSequence()
      .map(::AbilityFamilyPayload)
  }
  fun findAllByGuildIdAndFamilyId(guildId: String, familyId: Long) : Sequence<AbilityFamilyPayload> {
    return abilities_families
      .selectAll()
      .where({
        (abilities_families.guild_id eq guildId)
          .and(abilities_families.family_id eq familyId)
      })
      .asSequence()
      .map(::AbilityFamilyPayload)
  }
  fun createAbilityFamily(guildId: String, abilityId: Long, familyId: Long) : AbilityFamilyPayload {
    abilities_families.insert {
      it[this.guild_id] = guildId
      it[this.ability_id] = abilityId
      it[this.family_id] = familyId
    }
    return AbilityFamilyPayload(
      guildId = guildId,
      abilityId = abilityId,
      familyId = familyId
    )
  }
  fun deleteAbilityFamily(guildId: String, abilityId: Long, familyId: Long) : Unit {
    abilities_families.deleteWhere {
      (this.guild_id eq guildId)
        .and(this.ability_id eq abilityId)
        .and(this.family_id eq familyId)
    }
  }
}