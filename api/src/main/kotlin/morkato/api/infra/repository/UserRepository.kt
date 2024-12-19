package morkato.api.infra.repository

import org.jetbrains.exposed.sql.SqlExpressionBuilder.eq
import org.jetbrains.exposed.sql.deleteWhere
import org.jetbrains.exposed.sql.selectAll
import org.jetbrains.exposed.sql.ResultRow
import org.jetbrains.exposed.sql.update
import org.jetbrains.exposed.sql.insert
import org.jetbrains.exposed.sql.and
import morkato.api.exception.model.UserNotFoundError
import morkato.api.model.user.UserType
import morkato.api.infra.tables.users_abilities
import morkato.api.infra.tables.users_families
import morkato.api.infra.tables.users
import java.math.BigDecimal

object UserRepository {
  public data class UserPayload(
    val guildId: String,
    val id: String,
    val type: UserType,
    val flags: Int,
    val abilityRoll: BigDecimal,
    val familyRoll: BigDecimal,
    val prodigyRoll: BigDecimal,
    val markRoll: BigDecimal,
    val berserkRoll: BigDecimal
  ) {
    public constructor(row: ResultRow) : this(
      row[users.guild_id],
      row[users.id],
      row[users.type],
      row[users.flags],
      row[users.ability_roll],
      row[users.family_roll],
      row[users.prodigy_roll],
      row[users.mark_roll],
      row[users.berserk_roll]
    );
  }
  public data class UserAbilityPayload(
    val guildId: String,
    val userId: String,
    val abilityId: Long
  ) {
    public constructor(row: ResultRow) : this(
      row[users_abilities.guild_id],
      row[users_abilities.user_id],
      row[users_abilities.ability_id]
    );
  }
  public data class UserFamilyPayload(
    val guildId: String,
    val userId: String,
    val familyId: Long
  ) {
    public constructor(row: ResultRow) : this(
      row[users_families.guild_id],
      row[users_families.user_id],
      row[users_families.family_id]
    );
  }
  fun findById(guildId: String, id: String) : UserPayload {
    return try {
      UserPayload(
        users.selectAll()
          .where({
            (users.guild_id eq guildId)
              .and(users.id eq id)
          })
          .limit(1)
          .single()
      )
    } catch (exc: NoSuchElementException) {
      throw UserNotFoundError(guildId, id);
    }
  }
  fun createUser(
    guildId: String,
    id: String,
    type: UserType,
    flags: Int? = null,
    abilityRoll: BigDecimal? = null,
    familyRoll: BigDecimal? = null,
    prodigyRoll: BigDecimal? = null,
    markRoll: BigDecimal? = null,
    berserkRoll: BigDecimal? = null
  ) : UserPayload {
    users.insert {
      it[this.guild_id] = guildId
      it[this.id] = id
      it[this.type] = type
      if (flags != null) {
        it[this.flags] = flags
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
    }
    return UserPayload(
      guildId = guildId,
      id = id,
      type = type,
      flags = flags ?: 0,
      abilityRoll = abilityRoll ?: BigDecimal(3),
      familyRoll = familyRoll ?: BigDecimal(3),
      prodigyRoll = prodigyRoll ?: BigDecimal(1),
      markRoll = markRoll ?: BigDecimal(1),
      berserkRoll = berserkRoll ?: BigDecimal(1)
    )
  }
  fun updateUser(
    guildId: String,
    id: String,
    flags: Int? = null,
    abilityRoll: BigDecimal? = null,
    familyRoll: BigDecimal? = null,
    prodigyRoll: BigDecimal? = null,
    markRoll: BigDecimal? = null,
    berserkRoll: BigDecimal? = null
  ) : Unit {
    users.update({
      (users.guild_id eq guildId)
        .and(users.id eq id)
    }) {
      if (flags != null) {
        it[this.flags] = flags
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
    }
  }
  fun deleteUser(guildId: String, id: String) : Unit {
    users.deleteWhere {
      (this.guild_id eq guildId)
        .and(this.id eq id)
    }
  }
  fun getAllUserAbilities(guildId: String, id: String) : Sequence<UserAbilityPayload> {
    return users_abilities.selectAll()
      .where({
        (users_abilities.guild_id eq guildId)
          .and(users_abilities.user_id eq id)
      })
      .asSequence()
      .map(::UserAbilityPayload)
  }
  fun syncUserAbility(guildId: String, userId: String, abilityId: Long) : UserAbilityPayload {
    val user = this.findById(guildId, userId)
    users_abilities.insert {
      it[this.guild_id] = guildId
      it[this.user_id] = user.id
      it[this.ability_id] = abilityId
    }
    return UserAbilityPayload(
      guildId = guildId,
      userId = user.id,
      abilityId = abilityId
    )
  }
  fun getAllUserFamilies(guildId: String, id: String) : Sequence<UserFamilyPayload> {
    return users_families.selectAll()
      .where({
        (users_families.guild_id eq guildId)
          .and(users_families.user_id eq id)
      })
      .asSequence()
      .map(::UserFamilyPayload)
  }
  fun syncUserFamily(guildId: String, userId: String, familyId: Long) : UserFamilyPayload {
    val user = this.findById(guildId, userId)
    users_families.insert {
      it[this.guild_id] = guildId
      it[this.user_id] = user.id
      it[this.family_id] = familyId
    }
    return UserFamilyPayload(
      guildId = guildId,
      userId = user.id,
      familyId = familyId
    )
  }
}