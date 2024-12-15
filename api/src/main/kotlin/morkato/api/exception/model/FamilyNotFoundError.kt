package morkato.api.exception.model

import morkato.api.exception.GuildObjectNotFound
import morkato.api.exception.ModelType

class FamilyNotFoundError(
  guildId: String,
  id: String
) : GuildObjectNotFound(ModelType.FAMILY, guildId, id) {
}