package morkato.api.controller

import org.springframework.transaction.annotation.Transactional
import org.springframework.web.bind.annotation.RestController
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.DeleteMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.PutMapping
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestBody
import jakarta.validation.Valid

import morkato.api.infra.repository.GuildRepository
import morkato.api.model.guild.Guild
import morkato.api.dto.ability.AbilityResponseData
import morkato.api.dto.ability.AbilityCreateData
import morkato.api.dto.ability.AbilityUpdateData
import morkato.api.dto.validation.IdSchema
import morkato.api.exception.model.AbilityNotFoundError
import morkato.api.exception.model.GuildNotFoundError

@RestController
@RequestMapping("/abilities/{guild_id}")
class AbilityController {
  @GetMapping
  @Transactional
  fun getAllByGuildId(
    @PathVariable("guild_id") @IdSchema guild_id: String
  ) : List<AbilityResponseData>{
    val guild = Guild(GuildRepository.findById(guild_id))
    return guild.getAllAbilities()
      .map(::AbilityResponseData)
      .toList()
  }
  @PostMapping
  @Transactional
  fun createAbilityByGuildId(
    @PathVariable("guild_id") @IdSchema guild_id: String,
    @RequestBody @Valid data: AbilityCreateData
  ) : AbilityResponseData {
    val guild = Guild(GuildRepository.findById(guild_id))
    val ability = guild.createAbility(
      name = data.name,
      energy = data.energy,
      percent = data.percent,
      npcType = data.npc_type,
      description = data.description,
      banner = data.banner
    )
    return AbilityResponseData(ability)
  }
  @GetMapping("/{id}")
  @Transactional
  fun getReference(
    @PathVariable("guild_id") @IdSchema guild_id: String,
    @PathVariable("id") @IdSchema id: String
  ) : AbilityResponseData {
    val guild = Guild(GuildRepository.findById(guild_id))
    val ability = guild.getAbility(id.toLong())
    return AbilityResponseData(ability)
  }
  @PutMapping("/{id}")
  @Transactional
  fun updateAbilityByRef(
    @PathVariable("guild_id") @IdSchema guild_id: String,
    @PathVariable("id") @IdSchema id: String,
    @RequestBody @Valid data: AbilityUpdateData
  ) : AbilityResponseData {
    val guild = Guild(GuildRepository.findById(guild_id))
    val before = guild.getAbility(id.toLong())
    val ability = before.update(
      name = data.name,
      energy = data.energy,
      percent = data.percent,
      npcType = data.npc_type,
      description = data.description,
      banner = data.banner
    )
    return AbilityResponseData(ability)
  }
  @DeleteMapping("/{id}")
  @Transactional
  fun deleteAbilityByRef(
    @PathVariable("guild_id") @IdSchema guild_id: String,
    @PathVariable("id") @IdSchema id: String
  ) : AbilityResponseData {
    val guild = Guild(GuildRepository.findById(guild_id))
    val ability = guild.getAbility(id.toLong())
    ability.delete()
    return AbilityResponseData(ability)
  }
}