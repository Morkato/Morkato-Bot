package morkato.api.dto.player

import morkato.api.infra.repository.PlayerFamilyRepository

data class PlayerFamilyResponseData(
  val guild_id: String,
  val player_id: String,
  val family_id: String
) {
  public constructor(payload: PlayerFamilyRepository.PlayerFamilyPayload) : this(
    payload.guildId,
    payload.playerId,
    payload.familyId.toString()
  )
}
