package morkato.api.infra.tables

import org.jetbrains.exposed.sql.Table

object users_families : Table("users_families") {
  val guild_id = discordSnowflakeIdType("guild_id")
  val user_id = discordSnowflakeIdType("user_id")
  val family_id = idType("family_id")
}