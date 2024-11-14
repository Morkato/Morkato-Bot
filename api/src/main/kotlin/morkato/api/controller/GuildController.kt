package morkato.api.controller

import org.springframework.transaction.annotation.Transactional
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.PutMapping
import org.springframework.web.bind.annotation.GetMapping
import jakarta.validation.Valid
import morkato.api.dto.guild.GuildCreateData

import morkato.api.exception.model.GuildNotFoundError
import morkato.api.dto.guild.GuildResponseData
import morkato.api.dto.guild.GuildUpdateData
import morkato.api.model.guild.Guild

import morkato.api.infra.repository.GuildRepository
import morkato.api.dto.validation.IdSchema
import org.springframework.web.bind.annotation.PostMapping

@RestController
@RequestMapping("/guilds/{id}")
class GuildController {
  @GetMapping
  @Transactional
  fun getGuildByReference(
    @PathVariable("id") @IdSchema id: String
  ) : GuildResponseData {
    val guild = Guild(GuildRepository.findById(id))
    return GuildResponseData(guild)
  }
  @PostMapping
  @Transactional
  fun createGuild(
    @PathVariable("id") @IdSchema id: String,
    @RequestBody @Valid data: GuildCreateData
  ) : GuildResponseData {
    val payload = GuildRepository.createGuild(
      id = id,
      rpgStartCalendar = data.start_rpg_calendar,
      rpgStartDate = data.start_rpg_date,
      humanInitialLife = data.human_initial_life,
      oniInitialLife = data.oni_initial_life,
      hybridInitialLife = data.hybrid_initial_life,
      breathInitial = data.breath_initial,
      bloodInitial = data.blood_initial,
      familyRoll = data.family_roll,
      abilityRoll = data.ability_roll,
      prodigyRoll = null,
      markRoll = null,
      rollCategoryId = data.roll_category_id,
      offCategoryId = data.off_category_id
    )
    val guild = Guild(payload)
    return GuildResponseData(guild)
  }
  @PutMapping
  @Transactional
  fun updateGuildByReference(
    @PathVariable("id") @IdSchema id: String,
    @RequestBody @Valid data: GuildUpdateData
  ) : GuildResponseData {
    val before = Guild(GuildRepository.findById(id))
    val guild = before.update(
      humanInitialLife = data.human_initial_life,
      oniInitialLife = data.oni_initial_life,
      hybridInitialLife = data.hybrid_initial_life,
      breathInitial = data.breath_initial,
      bloodInitial = data.blood_initial,
      familyRoll = data.family_roll,
      abilityRoll = data.ability_roll,
      prodigyRoll = null,
      markRoll = null,
      berserkRoll = null,
      rollCategoryId = data.roll_category_id,
      offCategoryId = data.off_category_id
    )
    return GuildResponseData(guild)
  }
}