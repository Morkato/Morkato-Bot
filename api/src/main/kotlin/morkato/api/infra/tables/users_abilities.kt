package morkato.api.infra.tables

import org.jetbrains.exposed.sql.Table

object users_abilities : Table("users_abilities") {
  val guild_id = discordSnowflakeIdType("guild_id")
  val user_id = discordSnowflakeIdType("user_id")
  val ability_id = idType("ability_id")
}