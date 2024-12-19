package morkato.api.infra.tables

import org.jetbrains.exposed.sql.Table

object users : Table("users") {
  val guild_id = discordSnowflakeIdType("guild_id")
  val id = discordSnowflakeIdType("id")

  val type = userType("type")
  val flags = integer("flags")
  val ability_roll = rollType("ability_roll")
  val family_roll = rollType("family_roll")
  val prodigy_roll = rollType("prodigy_roll")
  val mark_roll = rollType("mark_roll")
  val berserk_roll = rollType("berserk_roll")

  override val primaryKey = PrimaryKey(guild_id, id)
}