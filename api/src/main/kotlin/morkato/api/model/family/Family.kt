package morkato.api.model.family

import morkato.api.infra.repository.FamilyRepository
import morkato.api.model.guild.Guild
import org.jetbrains.exposed.sql.ResultRow
import java.math.BigDecimal

class Family(
  val guild: Guild,
  val id: Long,
  val name: String,
  val percent: BigDecimal,
  val userType: Int,
  val description: String?,
  val banner: String?
) {
  public constructor(guild: Guild, row: ResultRow) : this(guild, FamilyRepository.FamilyPayload(row));
  public constructor(guild: Guild, payload: FamilyRepository.FamilyPayload) : this(
    guild,
    payload.id,
    payload.name,
    payload.percent,
    payload.userType,
    payload.description,
    payload.banner
  );
  fun update(
    name: String?,
    percent: BigDecimal?,
    userType: Int?,
    description: String?,
    banner: String?
  ) : Family {
    FamilyRepository.updateFamily(
      guildId = this.guild.id,
      id = this.id,
      name = name,
      percent = percent,
      userType = userType,
      description = description,
      banner = banner
    )
    return Family(
      guild = this.guild,
      id = id,
      name = name ?: this.name,
      percent = percent ?: this.percent,
      userType = userType ?: this.userType,
      description = description ?: this.description,
      banner = banner ?: this.banner
    )
  }
  fun delete() : Unit {
    FamilyRepository.deleteFamily(this.guild.id, this.id)
  }
}