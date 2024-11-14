package morkato.api.infra.tables

import org.jetbrains.exposed.sql.Table

object players_abilities : Table("players_abilities") {
  val guild_id = discordSnowflakeIdType("guild_id")
  val player_id = discordSnowflakeIdType("player_id")
  val ability_id = idType("ability_id")

  override val primaryKey = PrimaryKey(guild_id, player_id, ability_id)
}