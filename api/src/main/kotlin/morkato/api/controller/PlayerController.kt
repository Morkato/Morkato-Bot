package morkato.api.controller

import org.springframework.transaction.annotation.Transactional
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.DeleteMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.PutMapping
import org.springframework.web.bind.annotation.GetMapping
import jakarta.validation.Valid

import morkato.api.dto.validation.IdSchema
import morkato.api.dto.player.PlayerAbilityResponseData
import morkato.api.dto.player.PlayerFamilyResponseData
import morkato.api.dto.player.PlayerNpcCreateData
import morkato.api.dto.player.PlayerResponseData
import morkato.api.dto.player.PlayerCreateData
import morkato.api.dto.player.PlayerUpdateData
import morkato.api.exception.model.GuildNotFoundError
import morkato.api.exception.model.PlayerNotFoundError
import morkato.api.infra.repository.GuildRepository
import morkato.api.infra.repository.PlayerAbilityRepository
import morkato.api.infra.repository.PlayerFamilyRepository
import morkato.api.model.guild.Guild
import org.springframework.context.annotation.Profile

@RestController
@RequestMapping("/players/{guild_id}/{id}")
@Profile("api")
class PlayerController {
  @GetMapping
  @Transactional
  fun getPlayerByReference(
    @PathVariable("guild_id") @IdSchema guild_id: String,
    @PathVariable("id") @IdSchema id: String
  ) : PlayerResponseData {
    return try {
      val guild = Guild(GuildRepository.findById(guild_id))
      val player = guild.getPlayer(id)
      val npc = player.getReferredNpc()
      val abilities = player.getAllAbilities()
        .map(PlayerAbilityRepository.PlayerAbilityPayload::abilityId)
        .map(Long::toString)
        .toList()
      val families = player.getAllFamilies()
        .map(PlayerFamilyRepository.PlayerFamilyPayload::familyId)
        .map(Long::toString)
        .toList()
      PlayerResponseData(player, abilities, families, npc)
    } catch (exc: GuildNotFoundError) {
      throw PlayerNotFoundError(guild_id, id)
    }
  }
  @PostMapping
  @Transactional
  fun createPlayerByGuild(
    @PathVariable("guild_id") @IdSchema guild_id: String,
    @PathVariable("id") @IdSchema id: String,
    @RequestBody @Valid data: PlayerCreateData
  ) : PlayerResponseData {
    val guild = Guild(GuildRepository.findOrCreate(guild_id))
    val player = guild.createPlayer(
      id = id,
      npcType = data.npc_type,
      familyId = null,
      abilityRoll = data.ability_roll,
      familyRoll = data.family_roll,
      prodigyRoll = data.prodigy_roll,
      markRoll = data.mark_roll,
      berserkRoll = data.berserk_roll,
      flags = data.flags
    )
    return PlayerResponseData(player, listOf(), listOf(), null)
  }
  @PostMapping("/npc")
  @Transactional
  fun createPlayerNpcByReference(
    @PathVariable("guild_id") @IdSchema guild_id: String,
    @PathVariable("id") @IdSchema id: String,
    @RequestBody @Valid data: PlayerNpcCreateData
  ) : PlayerResponseData {
    return try {
      val guild = Guild(GuildRepository.findById(guild_id))
      val player = guild.getPlayer(id)
      val abilities = player.getAllAbilities()
        .map(PlayerAbilityRepository.PlayerAbilityPayload::abilityId)
        .map(Long::toString)
        .toList()
      val families = player.getAllFamilies()
        .map(PlayerFamilyRepository.PlayerFamilyPayload::familyId)
        .map(Long::toString)
        .toList()
      val npc = player.createNpc(
        name = data.name,
        surname = data.surname,
        icon = data.icon
      )
      PlayerResponseData(player, abilities, families, npc)
    } catch (exc: GuildNotFoundError) {
      throw PlayerNotFoundError(guild_id, id)
    }
  }
  @PutMapping
  @Transactional
  fun updatePlayerByReference(
    @PathVariable("guild_id") @IdSchema guild_id: String,
    @PathVariable("id") @IdSchema id: String,
    @RequestBody @Valid data: PlayerUpdateData
  ) : PlayerResponseData {
    return try {
      val guild = Guild(GuildRepository.findById(guild_id))
      val before = guild.getPlayer(id)
      val player = before.update(
        familyId = data.family_id?.toLong(),
        abilityRoll = data.ability_roll,
        familyRoll = data.family_roll,
        prodigyRoll = data.prodigy_roll,
        markRoll = data.mark_roll,
        berserkRoll = data.berserk_roll,
        flags = data.flags
      )
      val npc = player.getReferredNpc()
      val abilities = player.getAllAbilities()
        .map(PlayerAbilityRepository.PlayerAbilityPayload::abilityId)
        .map(Long::toString)
        .toList()
      val families = player.getAllFamilies()
        .map(PlayerFamilyRepository.PlayerFamilyPayload::familyId)
        .map(Long::toString)
        .toList()
      PlayerResponseData(player, abilities, families, npc)
    } catch (exc: GuildNotFoundError) {
      throw PlayerNotFoundError(guild_id, id)
    }
  }
  @DeleteMapping
  @Transactional
  fun deletePlayerByReference(
    @PathVariable("guild_id") @IdSchema guild_id: String,
    @PathVariable("id") @IdSchema id: String
  ) : PlayerResponseData {
    return try {
      val guild = Guild(GuildRepository.findById(guild_id))
      val player = guild.getPlayer(id)
      val npc = player.getReferredNpc()
      val abilities = player.getAllAbilities()
        .map(PlayerAbilityRepository.PlayerAbilityPayload::abilityId)
        .map(Long::toString)
        .toList()
      val families = player.getAllFamilies()
        .map(PlayerFamilyRepository.PlayerFamilyPayload::familyId)
        .map(Long::toString)
        .toList()
      player.delete()
      PlayerResponseData(player, abilities, families, npc)
    } catch (exc: GuildNotFoundError) {
      throw PlayerNotFoundError(guild_id, id)
    }
  }
  @PostMapping("/abilities/{ability_id}")
  @Transactional
  fun syncPlayerAbility(
    @PathVariable("guild_id") @IdSchema guild_id: String,
    @PathVariable("id") @IdSchema id: String,
    @PathVariable("ability_id") @IdSchema ability_id: String
  ) : PlayerAbilityResponseData {
    return try {
      val guild = Guild(GuildRepository.findById(guild_id))
      val player = guild.getPlayer(id)
      PlayerAbilityResponseData(player.addAbility(ability_id.toLong()))
    } catch (exc: GuildNotFoundError) {
      throw PlayerNotFoundError(guild_id, id)
    }
  }
  @PostMapping("/families/{family_id}")
  @Transactional
  fun syncPlayerFamily(
    @PathVariable("guild_id") @IdSchema guild_id: String,
    @PathVariable("id") @IdSchema id: String,
    @PathVariable("family_id") @IdSchema family_id: String
  ) : PlayerFamilyResponseData {
    return try {
      val guild = Guild(GuildRepository.findById(guild_id))
      val player = guild.getPlayer(id)
      PlayerFamilyResponseData(player.addFamily(family_id.toLong()))
    } catch (exc: GuildNotFoundError) {
      throw PlayerNotFoundError(guild_id, id)
    }
  }
}
