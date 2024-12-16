package morkato.api.controller

import morkato.api.dto.guild.GuildResponseData
import morkato.api.model.guild.Guild
import morkato.api.dto.validation.IdSchema
import morkato.api.exception.model.GuildNotFoundError
import morkato.api.infra.repository.GuildRepository
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.context.annotation.Profile
import org.springframework.transaction.annotation.Transactional
import org.springframework.web.bind.annotation.PathVariable

@RestController
@RequestMapping("/guilds/{id}")
@Profile("api")
class GuildController {
  @GetMapping
  @Transactional
  fun getGuildByRef(
    @PathVariable("id") @IdSchema id: String
  ) : GuildResponseData {
    val payload = try {GuildRepository.findById(id)} catch (exc: GuildNotFoundError) {GuildRepository.virtual(id)}
    val guild = Guild(payload)
    return GuildResponseData(guild)
  }
}