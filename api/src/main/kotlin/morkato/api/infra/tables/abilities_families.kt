package morkato.api.infra.tables

import org.jetbrains.exposed.sql.Table

object abilities_families : Table("abilities_families") {
  val guild_id = discordSnowflakeIdType("guild_id")
  val ability_id = idType("ability_id")
  val family_id = idType("family_id")

  override val primaryKey = PrimaryKey(guild_id, ability_id, family_id)
}