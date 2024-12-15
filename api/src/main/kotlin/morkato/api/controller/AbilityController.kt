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
import org.springframework.context.annotation.Profile

@RestController
@RequestMapping("/abilities/{guild_id}")
@Profile("api")
class AbilityController {
  @GetMapping
  @Transactional
  fun getAllByGuildId(
    @PathVariable("guild_id") @IdSchema guild_id: String
  ) : List<AbilityResponseData>{
    return try {
      val guild = Guild(GuildRepository.findById(guild_id))
      guild.getAllAbilities()
        .map(::AbilityResponseData)
        .toList()
    } catch (exc: GuildNotFoundError) {
      listOf()
    }
  }
  @PostMapping
  @Transactional
  fun createAbilityByGuildId(
    @PathVariable("guild_id") @IdSchema guild_id: String,
    @RequestBody @Valid data: AbilityCreateData
  ) : AbilityResponseData {
    val guild = Guild(GuildRepository.findOrCreate(guild_id))
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
    return try {
      val guild = Guild(GuildRepository.findById(guild_id))
      val ability = guild.getAbility(id.toLong())
      AbilityResponseData(ability)
    } catch (exc: GuildNotFoundError) {
      throw AbilityNotFoundError(guild_id, id);
    }
  }
  @PutMapping("/{id}")
  @Transactional
  fun updateAbilityByRef(
    @PathVariable("guild_id") @IdSchema guild_id: String,
    @PathVariable("id") @IdSchema id: String,
    @RequestBody @Valid data: AbilityUpdateData
  ) : AbilityResponseData {
    return try {
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
      AbilityResponseData(ability)
    } catch (exc: GuildNotFoundError) {
      throw AbilityNotFoundError(guild_id, id)
    }
  }
  @DeleteMapping("/{id}")
  @Transactional
  fun deleteAbilityByRef(
    @PathVariable("guild_id") @IdSchema guild_id: String,
    @PathVariable("id") @IdSchema id: String
  ) : AbilityResponseData {
    return try {
      val guild = Guild(GuildRepository.findById(guild_id))
      val ability = guild.getAbility(id.toLong())
      ability.delete()
      AbilityResponseData(ability)
    } catch (exc: GuildNotFoundError) {
      throw AbilityNotFoundError(guild_id, id);
    }
  }
}