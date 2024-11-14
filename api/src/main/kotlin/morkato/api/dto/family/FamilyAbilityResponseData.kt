package morkato.api.dto.family

import morkato.api.infra.repository.AbilityFamilyRepository

data class FamilyAbilityResponseData(
  val guild_id: String,
  val family_id: String,
  val ability_id: String
) {
  public constructor(fa: AbilityFamilyRepository.AbilityFamilyPayload) : this(
    fa.guildId,
    fa.familyId.toString(),
    fa.abilityId.toString()
  );
}
