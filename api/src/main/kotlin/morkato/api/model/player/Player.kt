package morkato.api.model.player

import morkato.api.exception.model.PlayerFamilyIsNullError
import morkato.api.exception.model.NpcNotFoundError
import morkato.api.infra.repository.PlayerAbilityRepository
import morkato.api.infra.repository.PlayerFamilyRepository
import morkato.api.infra.repository.PlayerRepository
import morkato.api.infra.repository.NpcRepository
import morkato.api.model.guild.Guild
import morkato.api.model.npc.NpcType
import morkato.api.model.npc.Npc

import org.jetbrains.exposed.sql.ResultRow
import java.math.BigDecimal

class Player(
  val guild: Guild,
  val id: String,
  val npcType: NpcType,
  val familyId: Long?,
  val abilityRoll: BigDecimal,
  val familyRoll: BigDecimal,
  val prodigyRoll: BigDecimal,
  val markRoll: BigDecimal,
  val berserkRoll: BigDecimal,
  val flags: Int,
) {
  public constructor(guild: Guild, row: ResultRow) : this(guild, PlayerRepository.PlayerPayload(row));
  public constructor(guild: Guild, payload: PlayerRepository.PlayerPayload) : this(
    guild,
    payload.id,
    payload.npcType,
    payload.familyId,
    payload.abilityRoll,
    payload.familyRoll,
    payload.prodigyRoll,
    payload.markRoll,
    payload.berserkRoll,
    payload.flags
  );
  fun getReferredNpc() : Npc? {
    try {
      val payload = NpcRepository.findByPlayerId(this.guild.id, this.id)
      return Npc(this.guild, payload)
    } catch (exc: NpcNotFoundError) {
      return null
    }
  }

  fun createNpc(
    name: String,
    surname: String,
    icon: String?
  ) : Npc {
    val familyId = this.familyId ?: throw PlayerFamilyIsNullError(this.guild.id, this.id)
    val npc = this.guild.createNpc(
      playerId = this.id,
      name = name,
      surname = surname,
      type = this.npcType,
      familyId = familyId,
      flags = this.flags,
      icon = icon
    )
    return this.guild.getNpc(npc.id)
  }

  fun getAllAbilities() : Sequence<PlayerAbilityRepository.PlayerAbilityPayload> {
    return PlayerAbilityRepository.findAllByGuildIdAndPlayerId(this.guild.id, this.id)
  }

  fun getAllFamilies() : Sequence<PlayerFamilyRepository.PlayerFamilyPayload> {
    return PlayerFamilyRepository.findAllByGuildIdAndPlayerId(this.guild.id, this.id)
  }

  fun addAbility(id: Long) : PlayerAbilityRepository.PlayerAbilityPayload {
    val ability = PlayerAbilityRepository.createPLayerAbility(this.guild.id, this.id, id)
    this.update(abilityRoll = this.abilityRoll - BigDecimal(1))
    return ability
  }
  fun addFamily(id: Long) : PlayerFamilyRepository.PlayerFamilyPayload {
    val family = PlayerFamilyRepository.createPlayerFamily(this.guild.id, this.id, id)
    this.update(familyRoll = this.familyRoll - BigDecimal(1))
    return family
  }

  fun update(
    familyId: Long? = null,
    abilityRoll: BigDecimal? = null,
    familyRoll: BigDecimal? = null,
    prodigyRoll: BigDecimal? = null,
    markRoll: BigDecimal? = null,
    berserkRoll: BigDecimal? = null,
    flags: Int? = null
  ) : Player {
    PlayerRepository.updatePlayer(
      guildId = this.guild.id,
      id = this.id,
      familyId = familyId,
      abilityRoll = abilityRoll,
      familyRoll = familyRoll,
      prodigyRoll = prodigyRoll,
      markRoll = markRoll,
      berserkRoll = berserkRoll,
      flags = flags
    )
    return Player(
      guild = this.guild,
      id = this.id,
      npcType = this.npcType,
      familyId = this.familyId ?: familyId,
      abilityRoll = abilityRoll ?: this.abilityRoll,
      familyRoll = familyRoll ?: this.familyRoll,
      prodigyRoll = prodigyRoll ?: this.prodigyRoll,
      markRoll = markRoll ?: this.markRoll,
      berserkRoll = berserkRoll ?: this.berserkRoll,
      flags = flags ?: this.flags
    )
  }

  fun delete() : Player {
    PlayerRepository.deletePlayer(this.guild.id, this.id)
    return this
  }
}
