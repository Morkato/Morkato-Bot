package morkato.api.dto.npc

import morkato.api.dto.validation.AttrSchema
import java.math.BigDecimal

data class NpcArtUpdateData(
  @AttrSchema val exp: BigDecimal
);
