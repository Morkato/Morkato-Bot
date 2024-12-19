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
import org.springframework.context.annotation.Profile
import morkato.api.exception.model.AbilityNotFoundError
import morkato.api.exception.model.GuildNotFoundError
import morkato.api.infra.repository.GuildRepository
import morkato.api.dto.ability.AbilityResponseData
import morkato.api.dto.ability.AbilityCreateData
import morkato.api.dto.ability.AbilityUpdateData
import morkato.api.dto.validation.IdSchema
import morkato.api.model.guild.Guild

@RestController
@RequestMapping("/abilities/{guild_id}")
@Profile("api")
class AbilityController {
  @GetMapping
  @Transactional
  fun getAllByGuildId(
    @PathVariable("guild_id") @IdSchema guildId: String
  ) : List<AbilityResponseData> {
    return try {
      val guild = Guild(GuildRepository.findById(guildId))
      val abilities = guild.getAllAbilities()
      return abilities.map(::AbilityResponseData).toList()
    } catch (exc: GuildNotFoundError) {
      listOf()
    }
  }
  @GetMapping("/{id}")
  @Transactional
  fun getAbilityById(
    @PathVariable("guild_id") @IdSchema guildId: String,
    @PathVariable("id") @IdSchema id: String
  ) : AbilityResponseData {
    return try {
      val guild = Guild(GuildRepository.findOrCreate(guildId))
      val ability = guild.getAbility(id.toLong())
      AbilityResponseData(ability)
    } catch (exc: GuildNotFoundError) {
      throw AbilityNotFoundError(guildId, id)
    }
  }
  @PostMapping
  @Transactional
  fun createAbilityByGuildId(
    @PathVariable("guild_id") guildId: String,
    @RequestBody data: AbilityCreateData
  ) : AbilityResponseData {
    val guild = Guild(GuildRepository.findOrCreate(guildId))
    val ability = guild.createAbility(
      name = data.name,
      userType = data.user_type,
      percent = data.percent,
      description = data.description,
      banner = data.banner
    )
    return AbilityResponseData(ability)
  }
  @PutMapping("/{id}")
  @Transactional
  fun updateAbilityById(
    @PathVariable("guild_id") @IdSchema guildId: String,
    @PathVariable("id") @IdSchema id: String,
    @RequestBody data: AbilityUpdateData
  ) : AbilityResponseData {
    return try {
      val guild = Guild(GuildRepository.findOrCreate(guildId))
      val before = guild.getAbility(id.toLong())
      val ability = before.update(
        name = data.name,
        userType = data.user_type,
        percent = data.percent,
        description = data.description,
        banner = data.banner
      )
      AbilityResponseData(ability)
    } catch (exc: GuildNotFoundError) {
      throw AbilityNotFoundError(guildId, id)
    }
  }
  @DeleteMapping("/{id}")
  @Transactional
  fun delAbilityById(
    @PathVariable("guild_id") @IdSchema guildId: String,
    @PathVariable("id") @IdSchema id: String
  ) : AbilityResponseData {
    return try {
      val guild = Guild(GuildRepository.findOrCreate(guildId))
      val ability = guild.getAbility(id.toLong())
      ability.delete()
      AbilityResponseData(ability)
    } catch (exc: GuildNotFoundError) {
      throw AbilityNotFoundError(guildId, id)
    }
  }
}