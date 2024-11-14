package morkato.api

import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc
import org.springframework.transaction.annotation.Transactional
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.test.context.ActiveProfiles
import org.springframework.test.web.servlet.MockMvc
import org.springframework.test.web.servlet.put
import org.springframework.test.web.servlet.get
import org.springframework.http.MediaType
import com.fasterxml.jackson.databind.ObjectMapper
import org.junit.jupiter.api.DisplayName
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import org.flywaydb.core.Flyway

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Transactional
abstract class ApiApplicationTests(
  @Autowired val flyway: Flyway,
  @Autowired val mvc: MockMvc,
  @Autowired val mapper: ObjectMapper
) {
  @BeforeEach
  fun setup() {
    flyway.clean()
    flyway.migrate()
  }
}
