package morkato.api.dto.npc

import jakarta.validation.constraints.NotNull
import morkato.api.dto.validation.BannerSchema
import morkato.api.dto.validation.NameSchema
import morkato.api.dto.validation.KeySchema
import morkato.api.dto.validation.IdSchema
import morkato.api.model.npc.NpcType

data class NpcCreateData(
  @NotNull @NameSchema val name: String,
  @IdSchema @NotNull val family_id: String,
  @NotNull @KeySchema val surname: String,
  @NotNull val type: NpcType,
  val flags: Int?,
  @BannerSchema val icon: String?
);
