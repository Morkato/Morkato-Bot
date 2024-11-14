package morkato.api.exception.model

import morkato.api.exception.NotFoundError
import morkato.api.exception.ModelType

class FamilyNotFoundError(
  extra: Map<String, Any?>
) : NotFoundError(ModelType.FAMILY, extra) {
}