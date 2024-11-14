package morkato.api

import org.springframework.beans.factory.annotation.Autowired
import org.springframework.test.web.servlet.MockMvc
import org.springframework.test.web.servlet.post
import org.springframework.test.web.servlet.get
import org.springframework.http.MediaType

import com.fasterxml.jackson.databind.ObjectMapper
import morkato.api.database.npc.NpcType
import org.flywaydb.core.Flyway

import org.junit.jupiter.api.DisplayName
import org.junit.jupiter.api.Test

class PlayerControllerTests(
  @Autowired flyway: Flyway,
  @Autowired mvc: MockMvc,
  @Autowired mapper: ObjectMapper
) : ApiApplicationTests(flyway, mvc, mapper) {
  companion object {
    const val GUILD_ID = GuildControllerTests.DEFAULT_GUILD_ID
    const val ID = "1111111111111111"
    val DEFAULT_NPC_KIND = NpcType.HUMAN
  }
  private val guildControllerTests = GuildControllerTests(flyway, mvc, mapper)
  @DisplayName("PlayerController endpoints")
  @Test
  fun playerControllerEndpoints() {
    val guild = guildControllerTests.getGuild()
    mvc.post("/players/$GUILD_ID/$ID") {
      val body: MutableMap<String, Any?> = mutableMapOf()
      body.put("expected_npc_kind", DEFAULT_NPC_KIND.name)
      contentType = MediaType.APPLICATION_JSON
      content = mapper.writeValueAsString(body)
    }.andExpect {
      status { isOk() }
      content { contentType(MediaType.APPLICATION_JSON) }
      jsonPath("$.guild_id") { value(GUILD_ID) }
      jsonPath("$.id") { value(ID) }
      jsonPath("$.ability_roll") { value(guild.ability_roll) }
      jsonPath("$.family_roll") { value(guild.family_roll) }
      jsonPath("$.is_prodigy") { value(false) }
      jsonPath("$.has_mark") { value(false) }
      jsonPath("$.expected_npc_type") { value(DEFAULT_NPC_KIND.name) }
      jsonPath("$.family_id") { value(null) }
      jsonPath("$.abilities.length()") { value(0) }
      jsonPath("$.families.length()") { value(0) }
      jsonPath("$.npc") { value(null) }
    }
  }
}