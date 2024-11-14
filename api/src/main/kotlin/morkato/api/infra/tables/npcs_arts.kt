package morkato.api.infra.tables

import org.jetbrains.exposed.sql.Table

object npcs_arts : Table("npcs_arts") {
  val guild_id = discordSnowflakeIdType("guild_id")
  val npc_id = idType("npc_id")
  val art_id = idType("art_id")
  val exp = attrType("exp")

  override val primaryKey = PrimaryKey(guild_id, npc_id, art_id)
}