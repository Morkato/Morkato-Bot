package morkato.api.infra.tables

import org.jetbrains.exposed.sql.Table

object abilities : Table("abilities") {
  val name = nameType("name")
  val percent = percentType("percent")
  val user_type = integer("user_type")
  val description = descriptionType("description").nullable()
  val banner = bannerType("banner").nullable()

  val guild_id = discordSnowflakeIdType("guild_id")
  val id = idType("id").autoIncrement()

  override val primaryKey = PrimaryKey(guild_id, id)
}