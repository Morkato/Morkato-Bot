package morkato.api

import org.springframework.beans.factory.annotation.Autowired
import org.springframework.test.web.servlet.MockMvc
import com.fasterxml.jackson.databind.ObjectMapper
import morkato.api.response.data.GuildResponseData
import org.springframework.test.web.servlet.get
import org.springframework.test.web.servlet.put
import org.springframework.http.MediaType
import org.junit.jupiter.api.DisplayName
import org.junit.jupiter.api.Test
import org.flywaydb.core.Flyway

class GuildControllerTests(
  @Autowired flyway: Flyway,
  @Autowired mvc: MockMvc,
  @Autowired mapper: ObjectMapper
) : ApiApplicationTests(flyway, mvc, mapper) {
  companion object {
    const val DEFAULT_GUILD_ID = "1111111111111111"
    const val DEFAULT_HUMAN_INITIAL_LIFE = 1000
    const val DEFAULT_ONI_INITIAL_LIFE = 500
    const val DEFAULT_HYBRID_INITIAL_LIFE = 1500
    const val DEFAULT_INITIAL_BREATH = 500
    const val DEFAULT_INITIAL_BLOOD = 1000
    const val DEFAULT_FAMILY_ROLL = 3
    const val DEFAULT_ABILITY_ROLL = 3

    const val ROLL_CATEGORY_ON_PUT_GUILD = "999999999999999"
    const val OFF_CATEGORY_ON_PUT_GUILD = "88888888888888888"
  }
  @Test
  @DisplayName("GuildController endpoints")
  fun guildControllerEndpoints() {
    this.getGuild()
    this.putGuild()
    this.getGuildAfterPut()
  }
  fun getGuild() : GuildResponseData {
    return mapper.readValue(
      mvc.get("/guilds/$DEFAULT_GUILD_ID")
        .andExpect {
          status { isOk() }
          content { contentType(MediaType.APPLICATION_JSON) }
          jsonPath("$.id") { value(DEFAULT_GUILD_ID) }
          jsonPath("$.human_initial_life") { value(DEFAULT_HUMAN_INITIAL_LIFE) }
          jsonPath("$.oni_initial_life") { value(DEFAULT_ONI_INITIAL_LIFE) }
          jsonPath("$.hybrid_initial_life") { value(DEFAULT_HYBRID_INITIAL_LIFE) }
          jsonPath("$.breath_initial") { value(DEFAULT_INITIAL_BREATH) }
          jsonPath("$.blood_initial") { value(DEFAULT_INITIAL_BLOOD) }
          jsonPath("$.family_roll") { value(DEFAULT_FAMILY_ROLL) }
          jsonPath("$.ability_roll") { value(DEFAULT_ABILITY_ROLL) }
          jsonPath("$.roll_category_id") { value(null) }
          jsonPath("$.off_category_id") { value(null) }
        }.andReturn()
        .response
        .contentAsString,
      GuildResponseData::class.java
    )
  }
    fun putGuild() : GuildResponseData {
      return mapper.readValue(
        mvc.put("/guilds/$DEFAULT_GUILD_ID") {
          val body: MutableMap<String, Any?> = mutableMapOf()
          body.put("roll_category_id", ROLL_CATEGORY_ON_PUT_GUILD)
          body.put("off_category_id", OFF_CATEGORY_ON_PUT_GUILD)

          contentType = MediaType.APPLICATION_JSON
          content = mapper.writeValueAsString(body)
        }.andExpect {
          status { isOk() }
          content { contentType(MediaType.APPLICATION_JSON) }
          jsonPath("$.id") { value(DEFAULT_GUILD_ID) }
          jsonPath("$.roll_category_id") { value(ROLL_CATEGORY_ON_PUT_GUILD) }
          jsonPath("$.off_category_id") { value(OFF_CATEGORY_ON_PUT_GUILD) }
        }.andReturn()
          .response
          .contentAsString,
        GuildResponseData::class.java
      )
  }
  fun getGuildAfterPut() : GuildResponseData {
    return mapper.readValue(
      mvc.get("/guilds/$DEFAULT_GUILD_ID")
        .andExpect {
          status { isOk() }
          content { contentType(MediaType.APPLICATION_JSON) }
          jsonPath("$.id") { value(DEFAULT_GUILD_ID) }
          jsonPath("$.human_initial_life") { value(DEFAULT_HUMAN_INITIAL_LIFE) }
          jsonPath("$.oni_initial_life") { value(DEFAULT_ONI_INITIAL_LIFE) }
          jsonPath("$.hybrid_initial_life") { value(DEFAULT_HYBRID_INITIAL_LIFE) }
          jsonPath("$.breath_initial") { value(DEFAULT_INITIAL_BREATH) }
          jsonPath("$.blood_initial") { value(DEFAULT_INITIAL_BLOOD) }
          jsonPath("$.family_roll") { value(DEFAULT_FAMILY_ROLL) }
          jsonPath("$.ability_roll") { value(DEFAULT_ABILITY_ROLL) }
          jsonPath("$.roll_category_id") { value(ROLL_CATEGORY_ON_PUT_GUILD) }
          jsonPath("$.off_category_id") { value(OFF_CATEGORY_ON_PUT_GUILD) }
        }.andReturn()
        .response
        .contentAsString,
      GuildResponseData::class.java
    )
  }
}