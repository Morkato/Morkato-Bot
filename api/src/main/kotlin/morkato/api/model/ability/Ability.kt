package morkato.api.model.ability

import morkato.api.infra.repository.AbilityRepository
import morkato.api.model.guild.Guild

import org.jetbrains.exposed.sql.ResultRow
import java.math.BigDecimal

class Ability(
  val guild: Guild,
  val id: Long,
  val name: String,
  val energy: BigDecimal,
  val percent: BigDecimal,
  val npcType: Int,
  val description: String?,
  val banner: String?
) {
  public constructor(guild: Guild, row: ResultRow) : this(guild, AbilityRepository.AbilityPayload(row)) {}
  public constructor(guild: Guild, payload: AbilityRepository.AbilityPayload) : this(
    guild,
    payload.id,
    payload.name,
    payload.energy,
    payload.percent,
    payload.npcType,
    payload.description,
    payload.banner
  );

  fun update(
    name: String?,
    energy: BigDecimal?,
    percent: BigDecimal?,
    npcType: Int?,
    description: String?,
    banner: String?
  ) : Ability {
    val payload = AbilityRepository.AbilityPayload(
      guildId = this.guild.id,
      id = this.id,
      name = name ?: this.name,
      energy = energy ?: this.energy,
      percent = percent ?: this.percent,
      npcType = npcType ?: this.npcType,
      description = description ?: this.description,
      banner = banner ?: this.banner
    )
    AbilityRepository.updateAbility(
      guildId = this.guild.id,
      id = this.id,
      name = name,
      energy = energy,
      percent = percent,
      npcType = npcType,
      description = description,
      banner = banner
    )
    return Ability(this.guild, payload)
  }

  fun delete() : Ability {
    AbilityRepository.deleteAbility(this.guild.id, this.id)
    return this
  }
}