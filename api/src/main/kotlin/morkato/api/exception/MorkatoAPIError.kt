package morkato.api.exception

import org.springframework.http.HttpStatusCode

open class MorkatoAPIError(
  val type: MorkatoAPIErrorType,
  val status: HttpStatusCode
) : Exception() {}