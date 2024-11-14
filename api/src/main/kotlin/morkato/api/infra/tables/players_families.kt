package morkato.api.infra.tables

import org.jetbrains.exposed.sql.Table

object players_families : Table("players_families") {
  val guild_id = discordSnowflakeIdType("guild_id")
  val player_id = discordSnowflakeIdType("player_id")
  val family_id = idType("family_id")

  override val primaryKey = PrimaryKey(guild_id, player_id, family_id)
}