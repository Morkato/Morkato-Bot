package morkato.api.exception.model

import morkato.api.exception.ModelType
import morkato.api.exception.NotFoundError

class ArtNotFoundError(
  extra: Map<String, Any?>
) : NotFoundError(ModelType.ART, extra) {
}