package morkato.api.exception.model

import morkato.api.exception.NotFoundError
import morkato.api.exception.ModelType

class PlayerNotFoundError(
  extra: Map<String, Any?>
) : NotFoundError(ModelType.PLAYER, extra) {
}
