package morkato.api.exception.model

import morkato.api.exception.GuildObjectNotFound
import morkato.api.exception.NotFoundError
import morkato.api.exception.ModelType

class AbilityNotFoundError(
  guildId: String,
  id: String
) : GuildObjectNotFound(ModelType.ABILITY, guildId, id) {
}