package morkato.api.controller

import org.springframework.transaction.annotation.Transactional
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.DeleteMapping
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.PutMapping
import org.springframework.web.bind.annotation.GetMapping
import jakarta.validation.Valid

import morkato.api.infra.repository.NpcAbilityRepository
import morkato.api.infra.repository.GuildRepository
import morkato.api.exception.model.GuildNotFoundError
import morkato.api.exception.model.NpcNotFoundError
import morkato.api.dto.validation.IdSchema
import morkato.api.dto.npc.NpcArtUpdateData
import morkato.api.dto.npc.NpcResponseData
import morkato.api.dto.npc.NpcCreateData
import morkato.api.dto.npc.NpcUpdateData
import morkato.api.model.guild.Guild
import java.time.Instant

@RestController
@RequestMapping("/npcs/{guild_id}")
class NpcController {
  @GetMapping("/{id}")
  @Transactional
  fun getReferenceByIdOrSurname(
    @PathVariable("guild_id") @IdSchema guild_id: String,
    @PathVariable("id") id: String
  ) : NpcResponseData {
    val guild = Guild(GuildRepository.findById(guild_id))
    val npc = if ("^[0-9]{15,30}$".toRegex().containsMatchIn(id))
      guild.getNpc(id.toLong())
    else guild.getNpcBySurname(id)
    val abilities = npc.getAllAbilities()
      .map(NpcAbilityRepository.NpcAbilityPayload::abilityId)
      .map(Long::toString)
      .toList()
    val arts = npc.getAllArts()
      .map { it.artId.toString() to it.exp }
      .toMap()
    return NpcResponseData(npc, abilities, arts)
  }
  @PostMapping
  @Transactional
  fun createNpcByGuild(
    @PathVariable("guild_id") @IdSchema guild_id: String,
    @RequestBody @Valid data: NpcCreateData
  ) : NpcResponseData {
    val guild = Guild(GuildRepository.findById(guild_id))
    val npc = guild.createNpc(
      name = data.name,
      type = data.type,
      familyId = data.family_id.toLong(),
      surname = data.surname,
      flags = data.flags,
      icon = data.icon
    )
    return NpcResponseData(npc, listOf(), mapOf())
  }
  @PutMapping("/{id}")
  @Transactional
  fun updateNpcByReference(
    @PathVariable("guild_id") @IdSchema guild_id: String,
    @PathVariable("id") @IdSchema id: String,
    @RequestBody @Valid data: NpcUpdateData
  ) : NpcResponseData {
    val guild = Guild(GuildRepository.findById(guild_id))
    val before = guild.getNpc(id.toLong())
    val npc = before.update(
      name = data.name,
      type = data.type,
      surname = data.surname,
      energy = data.energy,
      flags = data.flags,
      maxLife = data.max_life,
      maxBreath = data.max_breath,
      maxBlood = data.max_blood,
      currentLife = data.current_life,
      currentBreath = data.current_breath,
      currentBlood = data.current_blood,
      icon = data.icon,
      lastAction = if (data.last_action != null) Instant.ofEpochMilli(data.last_action) else null
    )
    val abilities = npc.getAllAbilities()
      .map(NpcAbilityRepository.NpcAbilityPayload::abilityId)
      .map(Long::toString)
      .toList()
    val arts = npc.getAllArts()
      .map { it.artId.toString() to it.exp }
      .toMap()
    return NpcResponseData(npc, abilities, arts)
  }
  @DeleteMapping("/{id}")
  @Transactional
  fun deleteNpcByReference(
    @PathVariable("guild_id") @IdSchema guild_id: String,
    @PathVariable("id") @IdSchema id: String
  ) : NpcResponseData {
    val guild = Guild(GuildRepository.findById(guild_id))
    val npc = guild.getNpc(id.toLong())
    val abilities = npc.getAllAbilities()
      .map(NpcAbilityRepository.NpcAbilityPayload::abilityId)
      .map(Long::toString)
      .toList()
    val arts = npc.getAllArts()
      .map { it.artId.toString() to it.exp }
      .toMap()
    npc.delete()
    return NpcResponseData(npc, abilities, arts)
  }
  @PutMapping("/{id}/arts/{art_id}")
  @Transactional
  fun updateNpcArt(
    @PathVariable("guild_id") @IdSchema guild_id: String,
    @PathVariable("id") @IdSchema id: String,
    @PathVariable("art_id") @IdSchema artId: String,
    data: NpcArtUpdateData
  ) : Unit {
    val guild = Guild(GuildRepository.findById(guild_id))
    val npc = guild.getNpc(id.toLong())
    npc.addArt(artId.toLong(), data.exp)
  }
}