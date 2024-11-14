package morkato.api.infra.tables

import morkato.api.model.ability.AbilityType
import org.jetbrains.exposed.sql.Table

object abilities : Table("abilities") {
  val guild_id = discordSnowflakeIdType("guild_id")
  val id = idType("id").autoIncrement()

  val name = nameType("name")
  val energy = energyType("energy")
  val percent = percentType("percent")
  val npc_type = integer("npc_type")
  val description = descriptionType("description").nullable()
  val banner = bannerType("banner").nullable()

  override val primaryKey = PrimaryKey(guild_id, id)
}