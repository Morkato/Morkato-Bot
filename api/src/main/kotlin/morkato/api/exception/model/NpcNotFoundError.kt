package morkato.api.exception.model

import morkato.api.exception.NotFoundError
import morkato.api.exception.ModelType

class NpcNotFoundError(
  extra: Map<String, Any?>
) : NotFoundError(ModelType.NPC, extra) {

}
