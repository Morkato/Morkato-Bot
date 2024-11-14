package morkato.api.dto.player

import morkato.api.infra.repository.PlayerAbilityRepository

data class PlayerAbilityResponseData(
  val guild_id: String,
  val player_id: String,
  val ability_id: String
) {
  public constructor(payload: PlayerAbilityRepository.PlayerAbilityPayload) : this(
    payload.guildId,
    payload.playerId,
    payload.abilityId.toString()
  )
}
