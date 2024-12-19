package morkato.api.model.guild

import morkato.api.infra.repository.*
import morkato.api.model.ability.Ability
import morkato.api.model.attack.Attack
import morkato.api.model.art.ArtType
import morkato.api.model.art.Art
import morkato.api.model.family.Family
import morkato.api.model.user.User
import morkato.api.model.user.UserType

import org.jetbrains.exposed.sql.ResultRow
import java.math.BigDecimal

class Guild(
  val id: String,
  val humanInitialLife: BigDecimal,
  val oniInitialLife: BigDecimal,
  val hybridInitialLife: BigDecimal,
  val breathInitial: BigDecimal,
  val bloodInitial: BigDecimal,
  val familyRoll: BigDecimal,
  val abilityRoll: BigDecimal,
  val prodigyRoll: BigDecimal,
  val markRoll: BigDecimal,
  val berserkRoll: BigDecimal,
  val rollCategoryId: String?,
  val offCategoryId: String?
) {
  public constructor(row: ResultRow) : this(GuildRepository.GuildPayload(row));
  public constructor(payload: GuildRepository.GuildPayload) : this(
    payload.id,
    payload.humanInitialLife,
    payload.oniInitialLife,
    payload.hybridInitialLife,
    payload.breathInitial,
    payload.bloodInitial,
    payload.familyRoll,
    payload.abilityRoll,
    payload.prodigyRoll,
    payload.markRoll,
    payload.berserkRoll,
    payload.rollCategoryId,
    payload.offCategoryId
  );
  fun update(
    humanInitialLife: BigDecimal?,
    oniInitialLife: BigDecimal?,
    hybridInitialLife: BigDecimal?,
    breathInitial: BigDecimal?,
    bloodInitial: BigDecimal?,
    familyRoll: BigDecimal?,
    abilityRoll: BigDecimal?,
    prodigyRoll: BigDecimal?,
    markRoll: BigDecimal?,
    berserkRoll: BigDecimal?,
    rollCategoryId: String?,
    offCategoryId: String?
  ) : Guild {
    val payload = GuildRepository.GuildPayload(
      id = this.id,
      humanInitialLife = humanInitialLife ?: this.humanInitialLife,
      oniInitialLife = oniInitialLife ?: this.oniInitialLife,
      hybridInitialLife = hybridInitialLife ?: this.hybridInitialLife,
      breathInitial = breathInitial ?: this.breathInitial,
      bloodInitial = bloodInitial ?: this.bloodInitial,
      familyRoll = familyRoll ?: this.familyRoll,
      abilityRoll = abilityRoll ?: this.abilityRoll,
      prodigyRoll = prodigyRoll ?: this.prodigyRoll,
      markRoll = markRoll ?: this.markRoll,
      berserkRoll = berserkRoll ?: this.berserkRoll,
      rollCategoryId = rollCategoryId ?: this.rollCategoryId,
      offCategoryId = offCategoryId ?: this.offCategoryId
    )
    GuildRepository.updateGuild(
      id = this.id,
      humanInitialLife = humanInitialLife,
      oniInitialLife = oniInitialLife,
      hybridInitialLife = hybridInitialLife,
      breathInitial = breathInitial,
      bloodInitial = bloodInitial,
      familyRoll = familyRoll,
      abilityRoll = abilityRoll,
      prodigyRoll = prodigyRoll,
      markRoll = markRoll,
      berserkRoll = berserkRoll,
      rollCategoryId = rollCategoryId,
      offCategoryId = offCategoryId
    )
    return Guild(payload)
  }
  fun getAllArts() : Sequence<Art> {
    return ArtRepository.findAllByGuildId(this.id)
      .map { Art(this@Guild, it) }
  }
  fun getArt(id: Long) : Art {
    val payload = ArtRepository.findById(this.id, id)
    return Art(this, payload)
  }
  fun createArt(
    name: String,
    type: ArtType,
    description: String?,
    banner: String?,
    energy: BigDecimal?,
    life: BigDecimal?,
    breath: BigDecimal?,
    blood: BigDecimal?
  ) : Art {
    val payload = ArtRepository.createArt(
      guildId = this.id,
      name = name,
      type = type,
      description = description,
      banner = banner,
      energy = energy,
      life = life,
      breath = breath,
      blood = blood
    )
    return Art(this, payload)
  }

  fun getAllAttacks() : Sequence<Attack> {
    return AttackRepository.findAllByGuildId(this.id)
      .map { Attack(this@Guild, it) }
  }
  fun getAttack(id: Long) : Attack {
    val payload = AttackRepository.findById(this.id, id)
    return Attack(this, payload)
  }

  fun getAllAbilities() : Sequence<Ability> {
    return AbilityRepository.findAllByGuildId(this.id)
      .map { Ability(this@Guild, it) }
  }
  fun getAbility(id: Long) : Ability {
    val payload = AbilityRepository.findById(this.id, id)
    return Ability(this, payload)
  }
  fun createAbility(
    name: String,
    userType: Int?,
    percent: BigDecimal?,
    description: String?,
    banner: String?
  ) : Ability {
    val payload = AbilityRepository.createAbility(
      guildId = this.id,
      name = name,
      userType = userType,
      percent = percent,
      description = description,
      banner = banner
    )
    return Ability(this, payload)
  }

  fun getAllFamilies() : Sequence<Family> {
    return FamilyRepository.findAllByGuildId(this.id)
      .map { Family(this@Guild, it) }
  }
  fun getFamily(id: Long) : Family {
    val payload = FamilyRepository.findById(this.id, id)
    return Family(this, payload)
  }
  fun createFamily(
    name: String,
    percent: BigDecimal?,
    userType: Int?,
    description: String?,
    banner: String?
  ) : Family {
    val payload = FamilyRepository.createFamily(
      guildId = this.id,
      name = name,
      percent = percent,
      userType = userType,
      description = description,
      banner = banner
    )
    return Family(this, payload)
  }

  fun getUser(id: String) : User {
    val payload = UserRepository.findById(this.id, id)
    return User(this, payload)
  }
  fun createUser(
    id: String,
    type: UserType,
    flags: Int? = null,
    abilityRoll: BigDecimal? = null,
    familyRoll: BigDecimal? = null,
    prodigyRoll: BigDecimal? = null,
    markRoll: BigDecimal? = null,
    berserkRoll: BigDecimal? = null
  ) : User {
    val payload = UserRepository.createUser(
      guildId = this.id,
      id = id,
      type = type,
      flags = flags,
      abilityRoll = abilityRoll,
      familyRoll = familyRoll,
      prodigyRoll = prodigyRoll,
      markRoll = markRoll,
      berserkRoll = berserkRoll
    )
    return User(this, payload)
  }
}