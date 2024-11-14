package morkato.api.infra.tables

import org.jetbrains.exposed.sql.javatime.timestamp
import org.jetbrains.exposed.sql.Table
import morkato.api.model.npc.NpcType

object npcs : Table("npcs") {
  val guild_id = discordSnowflakeIdType("guild_id")
  val id = idType("id").autoIncrement()

  val name = nameType("name")
  val type = npcType("type")
  val family_id = idType("family_id")
  val player_id = discordSnowflakeIdType("player_id").nullable()
  val surname = keyType("surname")
  val max_energy = energyType("max_energy").autoIncrement()
  val energy = energyType("energy")
  val flags = integer("flags")
  val max_life = attrType("max_life")
  val max_breath = attrType("max_breath")
  val max_blood = attrType("max_blood")
  val current_life = attrType("current_life")
  val current_breath = attrType("current_breath")
  val current_blood = attrType("current_blood")
  val icon = text("icon").nullable()
  val last_action = timestamp("last_action").nullable()

  override val primaryKey = PrimaryKey(guild_id, id)
}