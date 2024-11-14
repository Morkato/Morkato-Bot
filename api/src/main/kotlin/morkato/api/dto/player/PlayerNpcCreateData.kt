package morkato.api.dto.player

import jakarta.validation.constraints.NotNull
import morkato.api.dto.validation.BannerSchema
import morkato.api.dto.validation.NameSchema
import morkato.api.dto.validation.KeySchema

data class PlayerNpcCreateData(
  @NotNull @NameSchema val name: String,
  @NotNull @KeySchema val surname: String,
  @BannerSchema val icon: String?
);
