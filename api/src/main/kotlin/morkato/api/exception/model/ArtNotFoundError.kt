package morkato.api.exception.model

import morkato.api.exception.GuildObjectNotFound
import morkato.api.exception.ModelType

class ArtNotFoundError(
  guildId: String,
  id: String
) : GuildObjectNotFound(ModelType.ART, guildId, id) {
}