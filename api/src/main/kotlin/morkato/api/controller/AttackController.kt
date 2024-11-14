package morkato.api.controller

import org.springframework.transaction.annotation.Transactional
import org.springframework.web.bind.annotation.RestController
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.DeleteMapping
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.PutMapping
import org.springframework.web.bind.annotation.GetMapping

import morkato.api.exception.model.AttackNotFoundError
import morkato.api.exception.model.GuildNotFoundError
import morkato.api.exception.model.ArtNotFoundError
import morkato.api.infra.repository.GuildRepository
import morkato.api.model.guild.Guild
import morkato.api.dto.attack.AttackResponseData
import morkato.api.dto.attack.AttackCreateData
import morkato.api.dto.attack.AttackUpdateData
import morkato.api.dto.validation.IdSchema
import jakarta.validation.Valid

@RestController
@RequestMapping("/attacks/{guild_id}")
class AttackController {
  @GetMapping
  @Transactional
  fun getAllByGuildId(
    @PathVariable("guild_id") @IdSchema guild_id: String
  ) : List<AttackResponseData> {
    val guild = Guild(GuildRepository.findById(guild_id))
    return guild.getAllAttacks()
      .map(::AttackResponseData)
      .toList()
  }
  @GetMapping("/{id}")
  @Transactional
  fun getReference(
    @PathVariable("guild_id") @IdSchema guild_id: String,
    @PathVariable("id") @IdSchema id: String
  ) : AttackResponseData {
    val guild = Guild(GuildRepository.findById(guild_id))
    val attack = guild.getAttack(id.toLong())
    return AttackResponseData(attack)
  }
  @PostMapping("/{art_id}")
  @Transactional
  fun createAttackByArt(
    @PathVariable("guild_id") @IdSchema guild_id: String,
    @PathVariable("art_id") @IdSchema art_id: String,
    @RequestBody @Valid data: AttackCreateData
  ) : AttackResponseData {
    val guild = Guild(GuildRepository.findById(guild_id))
    val art = guild.getArt(art_id.toLong())
    val attack = art.createAttack(
      name = data.name,
      namePrefixArt = data.name_prefix_art,
      description = data.description,
      banner = data.banner,
      poisonTurn = data.poison_turn,
      burnTurn = data.burn_turn,
      bleedTurn = data.bleed_turn,
      poison = data.poison,
      burn = data.burn,
      bleed = data.bleed,
      stun = data.stun,
      damage = data.damage,
      breath = data.breath,
      blood = data.blood,
      flags = data.flags
    )
    return AttackResponseData(attack)
  }
  @PutMapping("/{id}")
  @Transactional
  fun updateAttackById(
    @PathVariable("guild_id") @IdSchema guild_id: String,
    @PathVariable("id") @IdSchema id: String,
    @RequestBody @Valid data: AttackUpdateData
  ) : AttackResponseData {
    val guild = Guild(GuildRepository.findById(guild_id))
    val before = guild.getAttack(id.toLong())
    val attack = before.update(
      name = data.name,
      namePrefixArt = data.name_prefix_art,
      description = data.description,
      banner = data.banner,
      poisonTurn = data.poison_turn,
      burnTurn = data.burn_turn,
      bleedTurn = data.bleed_turn,
      poison = data.poison,
      burn = data.burn,
      bleed = data.bleed,
      stun = data.stun,
      damage = data.damage,
      breath = data.breath,
      blood = data.blood,
      flags = data.flags
    )
    return AttackResponseData(attack)
  }
  @DeleteMapping("/{id}")
  @Transactional
  fun deleteByReference(
    @PathVariable("guild_id") @IdSchema guild_id: String,
    @PathVariable("id") @IdSchema id: String
  ) : AttackResponseData {
    val guild = Guild(GuildRepository.findById(guild_id))
    val attack = guild.getAttack(id.toLong())
    attack.delete()
    return AttackResponseData(attack)
  }
}
