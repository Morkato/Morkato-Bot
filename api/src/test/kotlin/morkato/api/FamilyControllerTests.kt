package morkato.api

import org.springframework.beans.factory.annotation.Autowired
import org.springframework.test.web.servlet.MockMvc
import com.fasterxml.jackson.databind.ObjectMapper
import morkato.api.database.npc.NpcType
import morkato.api.exception.ModelType
import morkato.api.response.data.FamilyResponseData
import org.springframework.test.web.servlet.post
import org.springframework.test.web.servlet.get
import org.springframework.http.MediaType
import org.junit.jupiter.api.DisplayName
import org.junit.jupiter.api.Test
import org.flywaydb.core.Flyway

class FamilyControllerTests(
  @Autowired flyway: Flyway,
  @Autowired mvc: MockMvc,
  @Autowired mapper: ObjectMapper
) : ApiApplicationTests(flyway, mvc, mapper) {
  companion object {
    const val GUILD_ID = GuildControllerTests.DEFAULT_GUILD_ID
    const val TEST_ID = "1111111111111111"
    const val DEFAULT_PERCENT = 50

    const val ON_POST_NAME = "Teste"
    val ON_POST_NPC_KIND: NpcType = NpcType.HUMAN
  }
  @DisplayName("FamilyController endpoints")
  @Test
  fun familyControllerEndpoints() {
    mvc.get("/families/$GUILD_ID")
      .andExpect {
        status { isOk() }
        content { contentType(MediaType.APPLICATION_JSON) }
        jsonPath("$.length()") { value(0) }
      }
    val familyPost: FamilyResponseData = mapper.readValue(
      mvc.post("/families/$GUILD_ID") {
        val body: MutableMap<String, Any?> = mutableMapOf()
        body.put("name", ON_POST_NAME)
        body.put("npc_kind", ON_POST_NPC_KIND.name)
        contentType = MediaType.APPLICATION_JSON
        content = mapper.writeValueAsString(body)
      }.andExpect {
        status { isOk() }
        content { contentType(MediaType.APPLICATION_JSON) }
        jsonPath("$.guild_id") { value(GUILD_ID) }
        jsonPath("$.name") { value(ON_POST_NAME) }
        jsonPath("$.percent") { value(DEFAULT_PERCENT) }
        jsonPath("$.npc_kind") { value(ON_POST_NPC_KIND.name) }
        jsonPath("$.description") { value(null) }
        jsonPath("$.banner") { value(null) }
      }.andReturn()
        .response
        .contentAsString,
      FamilyResponseData::class.java
    )
    mvc.get("/families/$GUILD_ID/${familyPost.id}")
      .andExpect {
        status { isOk() }
        content { contentType(MediaType.APPLICATION_JSON) }
        jsonPath("$.guild_id") { value(familyPost.guild_id) }
        jsonPath("$.id") { value(familyPost.id) }
        jsonPath("$.name") { value(familyPost.name) }
        jsonPath("$.percent") { value(familyPost.percent) }
        jsonPath("$.npc_kind") { value(familyPost.npc_kind.name) }
        jsonPath("$.description") { value(familyPost.description) }
        jsonPath("$.banner") { value(familyPost.banner) }
      }
  }
  @DisplayName("FamilyController endpoints errors")
  @Test
  fun familyControllerEndpointsErrors() {
    mvc.get("/families/$GUILD_ID/$TEST_ID")
      .andExpect {
        status { isNotFound() }
        content { contentType(MediaType.APPLICATION_JSON) }
        jsonPath("$.model") { value(ModelType.FAMILY.name) }
        jsonPath("$.extra.guild_id") { value(GUILD_ID) }
        jsonPath("$.extra.id") { value(TEST_ID) }
      }
  }
}