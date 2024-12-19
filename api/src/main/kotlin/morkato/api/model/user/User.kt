package morkato.api.model.user

import morkato.api.infra.repository.UserRepository
import morkato.api.model.guild.Guild
import org.jetbrains.exposed.sql.ResultRow
import java.math.BigDecimal

class User(
  val guild: Guild,
  val id: String,
  val type: UserType,
  val flags: Int,
  val abilityRoll: BigDecimal,
  val familyRoll: BigDecimal,
  val prodigyRoll: BigDecimal,
  val markRoll: BigDecimal,
  val berserkRoll: BigDecimal
) {
  public constructor(guild: Guild, row: ResultRow) : this(guild, UserRepository.UserPayload(row));
  public constructor(guild: Guild, payload: UserRepository.UserPayload) : this(
    guild,
    payload.id,
    payload.type,
    payload.flags,
    payload.abilityRoll,
    payload.familyRoll,
    payload.prodigyRoll,
    payload.markRoll,
    payload.berserkRoll
  );

  fun getAllAbilities() : Sequence<Long> {
    return UserRepository.getAllUserAbilities(this.guild.id, this.id)
      .map(UserRepository.UserAbilityPayload::abilityId)
  }
  fun getAllFamilies() : Sequence<Long> {
    return UserRepository.getAllUserFamilies(this.guild.id, this.id)
      .map(UserRepository.UserFamilyPayload::familyId)
  }

  fun syncAbility(id: Long) : UserRepository.UserAbilityPayload {
    return UserRepository.syncUserAbility(this.guild.id, this.id, id)
  }

  fun syncFamily(id: Long) : UserRepository.UserFamilyPayload {
    return UserRepository.syncUserFamily(this.guild.id, this.id, id)
  }

  fun update(
    flags: Int? = null,
    abilityRoll: BigDecimal? = null,
    familyRoll: BigDecimal? = null,
    prodigyRoll: BigDecimal? = null,
    markRoll: BigDecimal? = null,
    berserkRoll: BigDecimal? = null
  ) : User {
    UserRepository.updateUser(
      guildId = this.guild.id,
      id = this.id,
      flags = flags,
      abilityRoll = abilityRoll,
      familyRoll = familyRoll,
      prodigyRoll = prodigyRoll,
      markRoll = markRoll,
      berserkRoll = berserkRoll
    )
    return User(
      guild = this.guild,
      id = this.id,
      type = this.type,
      flags = flags ?: this.flags,
      abilityRoll = abilityRoll ?: this.abilityRoll,
      familyRoll = familyRoll ?: this.familyRoll,
      prodigyRoll = prodigyRoll ?: this.prodigyRoll,
      markRoll = markRoll ?: this.markRoll,
      berserkRoll = berserkRoll ?: this.berserkRoll
    );
  }
  fun delete() : Unit {
    UserRepository.deleteUser(this.guild.id, this.id)
  }
}