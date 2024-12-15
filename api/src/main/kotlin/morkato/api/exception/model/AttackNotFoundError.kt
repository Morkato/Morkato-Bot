package morkato.api.exception.model

import morkato.api.exception.GuildObjectNotFound
import morkato.api.exception.ModelType

class AttackNotFoundError(
  guildId: String,
  id: String
) : GuildObjectNotFound(ModelType.ATTACK, guildId, id) {}