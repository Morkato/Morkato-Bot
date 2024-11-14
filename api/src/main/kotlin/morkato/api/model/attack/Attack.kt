package morkato.api.model.attack

import morkato.api.infra.repository.AttackRepository
import morkato.api.model.guild.Guild

import org.jetbrains.exposed.sql.ResultRow
import java.math.BigDecimal

class Attack(
  val guild: Guild,
  val id: Long,
  val name: String,
  val artId: Long,
  val namePrefixArt: String?,
  val description: String?,
  val banner: String?,
  val poisonTurn: BigDecimal,
  val burnTurn: BigDecimal,
  val bleedTurn: BigDecimal,
  val poison: BigDecimal,
  val burn: BigDecimal,
  val bleed: BigDecimal,
  val stun: BigDecimal,
  val damage: BigDecimal,
  val breath: BigDecimal,
  val blood: BigDecimal,
  val flags: Int
) {
  public constructor(guild: Guild, row: ResultRow) : this(guild, AttackRepository.AttackPayload(row)) {}
  public  constructor(guild: Guild, payload: AttackRepository.AttackPayload) : this(
    guild,
    payload.id,
    payload.name,
    payload.artId,
    payload.namePrefixArt,
    payload.description,
    payload.banner,
    payload.poisonTurn,
    payload.burnTurn,
    payload.bleedTurn,
    payload.poison,
    payload.burn,
    payload.bleed,
    payload.stun,
    payload.damage,
    payload.breath,
    payload.blood,
    payload.flags
  );
  fun update(
    name: String? = null,
    namePrefixArt: String? = null,
    description: String? = null,
    banner: String? = null,
    poisonTurn: BigDecimal? = null,
    burnTurn: BigDecimal? = null,
    bleedTurn: BigDecimal? = null,
    poison: BigDecimal? = null,
    burn: BigDecimal? = null,
    bleed: BigDecimal? = null,
    stun: BigDecimal? = null,
    damage: BigDecimal? = null,
    breath: BigDecimal? = null,
    blood: BigDecimal? = null,
    flags: Int? = null
  ) : Attack {
    val payload = AttackRepository.AttackPayload(
      guildId = this.guild.id,
      id = this.id,
      name = name ?: this.name,
      artId = this.artId,
      namePrefixArt = namePrefixArt ?: this.namePrefixArt,
      description = description ?: this.description,
      banner = banner ?: this.banner,
      poisonTurn = poisonTurn ?: this.poisonTurn,
      burnTurn = burnTurn ?: this.burnTurn,
      bleedTurn = bleedTurn ?: this.bleedTurn,
      poison = poison ?: this.poison,
      burn = burn ?: this.burn,
      bleed = bleed ?: this.bleed,
      stun = stun ?: this.stun,
      damage = damage ?: this.damage,
      breath = breath ?: this.breath,
      blood = blood ?: this.blood,
      flags = flags ?: this.flags
    )
    AttackRepository.updateAttack(
      guildId = this.guild.id,
      id = this.id,
      name = name,
      namePrefixArt = namePrefixArt,
      description = description,
      banner = banner,
      poisonTurn = poisonTurn,
      burnTurn = burnTurn,
      bleedTurn = bleedTurn,
      poison = poison,
      burn = burn,
      bleed = bleed,
      stun = stun,
      damage = damage,
      breath = breath,
      blood = blood,
      flags = flags
    )
    return Attack(this.guild, payload)
  }
  fun delete() : Attack {
    AttackRepository.deleteAttack(this.guild.id, this.id)
    return this
  }
}
