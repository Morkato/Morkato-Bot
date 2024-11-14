package morkato.api.infra.tables

import org.jetbrains.exposed.sql.javatime.timestamp
import org.jetbrains.exposed.sql.Table

object guilds : Table("guilds") {
  val id = discordSnowflakeIdType("id")

  val start_rpg_calendar = timestamp("start_rpg_calendar")
  val start_rpg_date = timestamp("start_rpg_date")
  val human_initial_life = attrType("human_initial_life")
  val oni_initial_life = attrType("oni_initial_life")
  val hybrid_initial_life = attrType("hybrid_initial_life")
  val breath_initial = attrType("breath_initial")
  val blood_initial = attrType("blood_initial")
  val family_roll = rollType("family_roll")
  val ability_roll = rollType("ability_roll")
  val prodigy_roll = rollType("prodigy_roll")
  val mark_roll = rollType("mark_roll")
  val berserk_roll = rollType("berserk_roll")
  val roll_category_id = discordSnowflakeIdType("roll_category_id").nullable()
  val off_category_id = discordSnowflakeIdType("off_category_id").nullable()

  override val primaryKey = PrimaryKey(id)
}