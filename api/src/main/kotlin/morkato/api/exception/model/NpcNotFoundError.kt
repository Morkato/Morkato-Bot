package morkato.api.exception.model

import morkato.api.exception.GuildObjectNotFound
import morkato.api.exception.ModelType

class NpcNotFoundError(
  guildId: String,
  id: String
) : GuildObjectNotFound(ModelType.NPC, guildId, id) {

}
