package morkato.api.infra.tables

import org.jetbrains.exposed.sql.Table
import morkato.api.model.art.ArtType

object arts : Table("arts") {
  val guild_id = discordSnowflakeIdType("guild_id")
  val id = idType("id").autoIncrement()

  val name = nameType("name")
  val type = artType("type")
  val energy = energyType("energy")
  val life = attrType("life")
  val breath = attrType("breath")
  val blood = attrType("blood")
  val description = descriptionType("description").nullable()
  val banner = bannerType("banner").nullable()

  override val primaryKey = PrimaryKey(guild_id, id)
}