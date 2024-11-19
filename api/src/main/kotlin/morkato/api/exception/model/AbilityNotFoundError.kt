package morkato.api.exception.model

import morkato.api.exception.NotFoundError
import morkato.api.exception.ModelType

class AbilityNotFoundError(
  extra: Map<String, Any?>
) : NotFoundError(ModelType.ABILITY, extra) {
}