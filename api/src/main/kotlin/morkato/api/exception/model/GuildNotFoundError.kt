package morkato.api.exception.model

import morkato.api.exception.ModelType
import morkato.api.exception.NotFoundError

class GuildNotFoundError(extra: Map<String, Any?>) : NotFoundError(ModelType.GUILD, extra) {
}