package morkato.api.exception.model

class PlayerFamilyIsNullError(
  val guildId: String,
  val id: String
) : Exception() {
}
