package morkato.api.model.npc

import morkato.api.infra.repository.NpcAbilityRepository
import morkato.api.infra.repository.NpcArtRepository
import morkato.api.infra.repository.NpcRepository
import morkato.api.model.guild.Guild

import org.jetbrains.exposed.sql.ResultRow
import java.math.BigDecimal
import java.time.Instant

class Npc(
  val guild: Guild,
  val id: Long,
  val name: String,
  val type: NpcType,
  val familyId: Long,
  val surname: String,
  val maxEnergy: BigDecimal,
  val energy: BigDecimal,
  val flags: Int,
  val maxLife: BigDecimal,
  val maxBreath: BigDecimal,
  val maxBlood: BigDecimal,
  val currentLife: BigDecimal,
  val currentBreath: BigDecimal,
  val currentBlood: BigDecimal,
  val icon: String?,
  val lastAction: Instant?
) {
  public constructor(guild: Guild, row: ResultRow) : this(guild, NpcRepository.NpcPayload(row));
  public constructor(guild: Guild, payload: NpcRepository.NpcPayload) : this(
    guild,
    payload.id,
    payload.name,
    payload.type,
    payload.familyId,
    payload.surname,
    payload.maxEnergy,
    payload.energy,
    payload.flags,
    payload.maxLife,
    payload.maxBreath,
    payload.maxBlood,
    payload.currentLife,
    payload.currentBreath,
    payload.currentBlood,
    payload.icon,
    payload.lastAction
  );
  fun getAllAbilities() : Sequence<NpcAbilityRepository.NpcAbilityPayload> {
    return NpcAbilityRepository.findAllByGuildIdAndNpcId(this.guild.id, this.id)
  }
  fun getAllArts() : Sequence<NpcArtRepository.NpcArtPayload> {
    return NpcArtRepository.getAllByGuildIdAndNpcId(this.guild.id, this.id)
  }
  fun addAbility(id: Long) : NpcAbilityRepository.NpcAbilityPayload {
    return NpcAbilityRepository.createNpcAbility(this.guild.id, this.id, id)
  }
  fun addArt(id: Long, exp: BigDecimal) : NpcArtRepository.NpcArtPayload {
    return NpcArtRepository.createOrUpdateNpcArt(this.guild.id, this.id, id, exp)
  }

  fun update(
    name: String?,
    type: NpcType?,
    surname: String?,
    energy: BigDecimal?,
    maxLife: BigDecimal?,
    maxBreath: BigDecimal?,
    maxBlood: BigDecimal?,
    currentLife: BigDecimal?,
    currentBreath: BigDecimal?,
    currentBlood: BigDecimal?,
    icon: String?,
    flags: Int?,
    lastAction: Instant?
  ) : Npc {
    NpcRepository.updateNpc(
      guildId = this.guild.id,
      id = this.id,
      name = name,
      type = type,
      surname = surname,
      maxEnergy = null,
      energy = energy,
      maxLife = maxLife,
      maxBreath = maxBreath,
      maxBlood = maxBlood,
      currentLife = currentLife,
      currentBreath = currentBreath,
      currentBlood = currentBlood,
      icon = icon,
      flags = flags,
      lastAction = lastAction
    )
    return Npc(
      guild = this.guild,
      id = this.id,
      name = name ?: this.name,
      type = type ?: this.type,
      familyId = this.familyId,
      surname = surname ?: this.surname,
      maxEnergy = this.maxEnergy,
      energy = energy ?: this.energy,
      maxLife = maxLife ?: this.maxLife,
      maxBreath = maxBreath ?: this.maxBreath,
      maxBlood = maxBlood ?: this.maxBlood,
      currentLife = currentLife ?: this.currentLife,
      currentBreath = currentBreath ?: this.currentBreath,
      currentBlood = currentBlood ?: this.currentBlood,
      icon = icon ?: this.icon,
      flags = flags ?: this.flags,
      lastAction = lastAction ?: this.lastAction
    )
  }
  fun delete() : Npc {
    NpcRepository.deleteNpc(guildId = this.guild.id, id = this.id)
    return this
  }
}