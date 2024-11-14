package morkato.api.infra.tables

import org.jetbrains.exposed.sql.Table

object npcs_abilities : Table("npcs_abilities") {
  val guild_id = discordSnowflakeIdType("guild_id")
  val npc_id = idType("npc_id")
  val ability_id = idType("ability_id")

  override val primaryKey = PrimaryKey(guild_id, npc_id, ability_id)
}