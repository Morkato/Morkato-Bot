package morkato.api.model.guild

import morkato.api.infra.repository.*

import morkato.api.model.ability.AbilityType
import morkato.api.model.ability.Ability
import morkato.api.model.family.Family
import morkato.api.model.attack.Attack
import morkato.api.model.player.Player
import morkato.api.model.npc.NpcType
import morkato.api.model.npc.Npc
import morkato.api.model.art.ArtType
import morkato.api.model.art.Art

import org.jetbrains.exposed.sql.ResultRow
import java.math.BigDecimal
import java.time.Instant

class Guild(
  val id: String,
  val startRpgCalendar: Instant,
  val startRpgDate: Instant,
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
    payload.startRpgCalendar,
    payload.startRpgDate,
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
      startRpgCalendar = this.startRpgCalendar,
      startRpgDate = this.startRpgDate,
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
      .map { Ability(this, it) }
  }
  fun getAbility(id: Long) : Ability {
    val payload = AbilityRepository.findById(this.id, id)
    return Ability(this, payload)
  }
  fun createAbility(
    name: String,
    energy: BigDecimal?,
    percent: BigDecimal?,
    npcType: Int,
    description: String?,
    banner: String?
  ) : Ability {
    val payload = AbilityRepository.createAbility(
      guildId = this.id,
      name = name,
      energy = energy,
      percent = percent,
      npcType = npcType,
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
    npcType: Int?,
    percent: BigDecimal?,
    description: String?,
    banner: String?
  ) : Family {
    val payload = FamilyRepository.createFamily(
      guildId = this.id,
      name = name,
      npcType = npcType,
      percent = percent,
      description = description,
      banner = banner
    )
    return Family(this, payload)
  }

  fun getAllAbilitiesFamilies() : Sequence<AbilityFamilyRepository.AbilityFamilyPayload> {
    return AbilityFamilyRepository.findAllByGuildId(this.id)
  }

  fun getNpc(id: Long) : Npc {
    val payload = NpcRepository.findById(this.id, id)
    return Npc(this, payload)
  }
  fun getNpcBySurname(surname: String) : Npc {
    val payload = NpcRepository.findBySurname(this.id, surname)
    return Npc(this, payload)
  }
  fun createNpc(
    playerId: String? = null,
    name: String,
    type: NpcType,
    familyId: Long,
    surname: String,
    flags: Int?,
    icon: String?
  ) : Npc {
    val life = when (type) {
      NpcType.HUMAN -> this.humanInitialLife
      NpcType.ONI -> this.oniInitialLife
      NpcType.HYBRID -> this.hybridInitialLife
    }
    val breath = this.breathInitial
    val blood = this.bloodInitial
    val payload = NpcRepository.createNpc(
      playerId = playerId,
      guildId = this.id,
      name = name,
      type = type,
      familyId = familyId,
      surname = surname,
      flags = flags,
      life = life,
      breath = breath,
      blood = blood,
      icon = icon
    )
    return Npc(this, payload)
  }

  fun getPlayer(id: String) : Player {
    val payload = PlayerRepository.findById(this.id, id)
    return Player(this, payload)
  }
  fun createPlayer(
    id: String,
    npcType: NpcType,
    familyId: Long?,
    abilityRoll: BigDecimal?,
    familyRoll: BigDecimal?,
    prodigyRoll: BigDecimal?,
    markRoll: BigDecimal?,
    berserkRoll: BigDecimal?,
    flags: Int?
  ) : Player {
    val thisAbilityRoll = abilityRoll ?: this@Guild.abilityRoll
    val thisFamilyRoll = familyRoll ?: this@Guild.familyRoll
    val thisProdigyRoll = prodigyRoll ?: this.prodigyRoll
    val thisMarkRoll = markRoll ?: this.markRoll
    val thisBerserkRoll = berserkRoll ?: this.berserkRoll
    val payload = PlayerRepository.createPlayer(
      this.id, id,
      npcType = npcType,
      familyId = familyId,
      abilityRoll = thisAbilityRoll,
      familyRoll = thisFamilyRoll,
      prodigyRoll = thisProdigyRoll,
      markRoll = thisMarkRoll,
      berserkRoll = thisBerserkRoll,
      flags = flags
    )
    return Player(this, payload)
  }
}