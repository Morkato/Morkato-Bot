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
import morkato.api.exception.model.FamilyNotFoundError
import morkato.api.exception.model.GuildNotFoundError
import morkato.api.infra.repository.GuildRepository
import morkato.api.dto.family.FamilyResponseData
import morkato.api.dto.family.FamilyUpdateData
import morkato.api.dto.family.FamilyCreateData
import morkato.api.dto.validation.IdSchema
import morkato.api.model.guild.Guild

@RestController
@RequestMapping("/families/{guild_id}")
@Profile("api")
class FamilyController {
  @GetMapping
  @Transactional
  fun getAllByGuildId(
    @PathVariable("guild_id") @IdSchema guildId: String
  ) : List<FamilyResponseData> {
    return try {
      val guild = Guild(GuildRepository.findById(guildId))
      val families = guild.getAllFamilies()
      families.map(::FamilyResponseData).toList()
    } catch (exc: GuildNotFoundError) {
      listOf()
    }
  }
  @GetMapping("/{id}")
  @Transactional
  fun getFamilyById(
    @PathVariable("guild_id") @IdSchema guildId: String,
    @PathVariable("id") @IdSchema id: String
  ) : FamilyResponseData {
    return try {
      val guild = Guild(GuildRepository.findById(guildId))
      val family = guild.getFamily(id.toLong())
      FamilyResponseData(family)
    } catch (exc: GuildNotFoundError) {
      throw FamilyNotFoundError(guildId, id)
    }
  }
  @PostMapping
  @Transactional
  fun createFamilyById(
    @PathVariable("guild_id") guildId: String,
    @RequestBody data: FamilyCreateData
  ) : FamilyResponseData {
    val guild = Guild(GuildRepository.findOrCreate(guildId))
    val family = guild.createFamily(
      name = data.name,
      percent = data.percent,
      userType = data.user_type,
      description = data.description,
      banner = data.banner
    )
    return FamilyResponseData(family)
  }
  @PutMapping("/{id}")
  @Transactional
  fun updateFamilyById(
    @PathVariable("guild_id") @IdSchema guildId: String,
    @PathVariable("id") @IdSchema id: String,
    @RequestBody data: FamilyUpdateData
  ) : FamilyResponseData {
    return try {
      val guild = Guild(GuildRepository.findById(guildId))
      val before = guild.getFamily(id.toLong())
      val family = before.update(
        name = data.name,
        percent = data.percent,
        userType = data.user_type,
        description = data.description,
        banner = data.banner
      )
      FamilyResponseData(family)
    } catch (exc: GuildNotFoundError) {
      throw FamilyNotFoundError(guildId, id)
    }
  }
  @DeleteMapping("/{id}")
  @Transactional
  fun delFamilyById(
    @PathVariable("guild_id") @IdSchema guildId: String,
    @PathVariable("id") @IdSchema id: String
  ) : FamilyResponseData {
    return try {
      val guild = Guild(GuildRepository.findById(guildId))
      val family = guild.getFamily(id.toLong())
      family.delete()
      FamilyResponseData(family)
    } catch (exc: GuildNotFoundError) {
      throw FamilyNotFoundError(guildId, id)
    }
  }
}