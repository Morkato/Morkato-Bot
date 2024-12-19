package morkato.api.infra.exception

import org.springframework.web.bind.annotation.RestControllerAdvice
import org.springframework.web.bind.annotation.ExceptionHandler
import org.springframework.http.ResponseEntity
import org.springframework.http.HttpStatus

import morkato.api.exception.NotFoundError

@RestControllerAdvice
class ErrorControllerHandler {
  @ExceptionHandler(NotFoundError::class)
  fun onNotFoundError(exc: NotFoundError) : ResponseEntity<Map<String, Any?>> {
    return ResponseEntity(exc.body(), HttpStatus.NOT_FOUND)
  }
}