package morkato.api.exception.model

import morkato.api.exception.ModelType
import morkato.api.exception.NotFoundError

class ImageNotFoundError(extra: Map<String, Any?>) : NotFoundError(ModelType.IMAGE, extra) {
}