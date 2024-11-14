package morkato.api.exception.model

import morkato.api.exception.NotFoundError
import morkato.api.exception.ModelType

class AttackNotFoundError(
  extra: Map<String, Any?>
) : NotFoundError(ModelType.ATTACK, extra) {}