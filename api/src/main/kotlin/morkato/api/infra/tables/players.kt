package morkato.api.infra.tables

import org.jetbrains.exposed.sql.Table

object players : Table("players") {
  val guild_id = discordSnowflakeIdType("guild_id")
  val id = discordSnowflakeIdType("id")

  val npc_type = npcType("npc_type")
  val family_id = idType("family_id",).nullable()
  val ability_roll = rollType("ability_roll")
  val family_roll = rollType("family_roll")
  val prodigy_roll = rollType("prodigy_roll")
  val mark_roll = rollType("mark_roll")
  val berserk_roll = rollType("berserk_roll")
  val flags = integer("flags")

  override val primaryKey = PrimaryKey(guild_id, id)
}