package morkato.api.model.ability

import morkato.api.infra.repository.AbilityRepository
import org.jetbrains.exposed.sql.ResultRow
import morkato.api.model.guild.Guild
import java.math.BigDecimal

class Ability(
  val guild: Guild,
  val id: Long,
  val name: String,
  val percent: BigDecimal,
  val userType: Int,
  val description: String?,
  val banner: String?
) {
  public constructor(guild: Guild, row: ResultRow) : this(guild, AbilityRepository.AbilityPayload(row));
  public constructor(guild: Guild, payload: AbilityRepository.AbilityPayload) : this(
    guild = guild,
    payload.id,
    payload.name,
    payload.percent,
    payload.userType,
    payload.description,
    payload.banner
  );
  fun update(
    name: String?,
    userType: Int?,
    percent: BigDecimal?,
    description: String?,
    banner: String?
  ) : Ability {
    AbilityRepository.updateAbility(
      guildId = this.guild.id,
      id = this.id,
      name = name,
      percent = percent,
      userType = userType,
      description = description,
      banner = banner
    )
    return Ability(
      guild = this.guild,
      id = this.id,
      name = name ?: this.name,
      percent = percent ?: this.percent,
      userType = userType ?: this.userType,
      description = description ?: this.description,
      banner = banner ?: this.banner
    )
  }
  fun delete() : Unit {
    AbilityRepository.deleteAbility(this.guild.id, this.id)
  }
}