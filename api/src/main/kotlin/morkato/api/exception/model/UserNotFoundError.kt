package morkato.api.exception.model

import morkato.api.exception.GuildObjectNotFound
import morkato.api.exception.ModelType

class UserNotFoundError(
  guildId: String,
  id: String
) : GuildObjectNotFound(ModelType.USER, guildId, id) {
}
