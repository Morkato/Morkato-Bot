package morkato.api

import org.springframework.beans.factory.annotation.Autowired
import org.springframework.test.web.servlet.MockMvc
import com.fasterxml.jackson.databind.ObjectMapper
import org.springframework.test.web.servlet.get
import org.springframework.test.web.servlet.put
import org.springframework.http.MediaType
import org.junit.jupiter.api.DisplayName
import org.junit.jupiter.api.Test
import org.flywaydb.core.Flyway

class AbilityTests(
  @Autowired flyway: Flyway,
  @Autowired mvc: MockMvc,
  @Autowired mapper: ObjectMapper
) : ApiApplicationTests(flyway, mvc, mapper) {
}