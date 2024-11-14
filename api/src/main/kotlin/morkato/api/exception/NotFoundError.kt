package morkato.api.exception

open class NotFoundError(
  val model: ModelType,
  val extra: Any? = null
) : Exception() {
  fun body() : Map<String, Any?> {
    return mapOf(
      "model" to model.name,
      "extra" to extra
    )
  }
}