package morkato.api.exception.model

import morkato.api.exception.GuildObjectNotFound
import morkato.api.exception.ModelType

class PlayerNotFoundError(
  guildId: String,
  id: String
) : GuildObjectNotFound(ModelType.PLAYER, guildId, id) {
}
