package morkato.api.infra.repository

import org.jetbrains.exposed.sql.ResultRow
import org.jetbrains.exposed.sql.selectAll
import org.jetbrains.exposed.sql.insert
import org.jetbrains.exposed.sql.update

import morkato.api.exception.model.GuildNotFoundError
import morkato.api.infra.tables.guilds
import java.math.RoundingMode
import java.math.BigDecimal
import java.time.Instant

object GuildRepository {
  public data class GuildPayload(
    val id: String,
    val startRpgCalendar: Instant,
    val startRpgDate: Instant,
    val humanInitialLife: BigDecimal,
    val oniInitialLife: BigDecimal,
    val hybridInitialLife: BigDecimal,
    val breathInitial: BigDecimal,
    val bloodInitial: BigDecimal,
    val familyRoll: BigDecimal,
    val abilityRoll: BigDecimal,
    val prodigyRoll: BigDecimal,
    val markRoll: BigDecimal,
    val berserkRoll: BigDecimal,
    val rollCategoryId: String?,
    val offCategoryId: String?
  ) {
    public constructor(row: ResultRow) : this(
      row[guilds.id],
      row[guilds.start_rpg_calendar],
      row[guilds.start_rpg_date],
      row[guilds.human_initial_life],
      row[guilds.oni_initial_life],
      row[guilds.hybrid_initial_life],
      row[guilds.breath_initial],
      row[guilds.blood_initial],
      row[guilds.family_roll],
      row[guilds.ability_roll],
      row[guilds.prodigy_roll],
      row[guilds.mark_roll],
      row[guilds.berserk_roll],
      row[guilds.roll_category_id],
      row[guilds.off_category_id]
    ) {}
  }
  private object DefaultValue {
    val humanInitialLife = BigDecimal(1000).setScale(12, RoundingMode.UP)
    val oniInitialLife = BigDecimal(500).setScale(12, RoundingMode.UP)
    val hybridInitialLife = BigDecimal(1500).setScale(12, RoundingMode.UP)
    val breathInitial = BigDecimal(500).setScale(12, RoundingMode.UP)
    val bloodInitial = BigDecimal(1000).setScale(12, RoundingMode.UP)
    val familyRoll = BigDecimal(3).setScale(3, RoundingMode.UP)
    val abilityRoll = BigDecimal(3).setScale(3, RoundingMode.UP)
    val prodigyRoll = BigDecimal(1).setScale(3, RoundingMode.UP)
    val markRoll = BigDecimal(1).setScale(3, RoundingMode.UP)
    val berserkRoll = BigDecimal(1).setScale(3, RoundingMode.UP)
  }
  fun findById(id: String) : GuildPayload {
    return try {
      GuildPayload(
        guilds
          .selectAll()
          .where({ guilds.id eq id })
          .limit(1)
          .single()
      )
    } catch (exc: NoSuchElementException) {
      val extra: Map<String, Any?> = mapOf("id" to id)
      throw GuildNotFoundError(extra)
    }
  }
  fun   createGuild(
    id: String,
    rpgStartCalendar: Instant,
    rpgStartDate: Instant? = null,
    humanInitialLife: BigDecimal? = null,
    oniInitialLife: BigDecimal? = null,
    hybridInitialLife: BigDecimal? = null,
    breathInitial: BigDecimal? = null,
    bloodInitial: BigDecimal? = null,
    familyRoll: BigDecimal? = null,
    abilityRoll: BigDecimal? = null,
    prodigyRoll: BigDecimal? = null,
    markRoll: BigDecimal? = null,
    berserkRoll: BigDecimal? = null,
    rollCategoryId: String? = null,
    offCategoryId: String? = null
  ) : GuildPayload {
    guilds.insert {
      it[this.id] = id
      it[this.roll_category_id] = rollCategoryId
      it[this.off_category_id] = offCategoryId
      it[this.start_rpg_calendar] = rpgStartCalendar
      if (rpgStartDate != null) {
        it[this.start_rpg_date] = rpgStartDate
      }
      if (humanInitialLife != null) {
        it[this.human_initial_life] = humanInitialLife
      }
      if (oniInitialLife != null) {
        it[this.oni_initial_life] = oniInitialLife
      }
      if (hybridInitialLife != null) {
        it[this.hybrid_initial_life] = hybridInitialLife
      }
      if (breathInitial != null) {
        it[this.breath_initial] = breathInitial
      }
      if (bloodInitial != null) {
        it[this.blood_initial] = bloodInitial
      }
      if (familyRoll != null) {
        it[this.family_roll] = familyRoll
      }
      if (abilityRoll != null) {
        it[this.ability_roll] = abilityRoll
      }
      if (prodigyRoll != null) {
        it[this.prodigy_roll] = prodigyRoll
      }
      if (markRoll != null) {
        it[this.mark_roll] = markRoll
      }
      if (berserkRoll != null) {
        it[this.berserk_roll] = berserkRoll
      }
    }
    return GuildPayload(
      id = id,
      startRpgCalendar = rpgStartCalendar,
      startRpgDate = rpgStartDate ?: Instant.now(),
      humanInitialLife = humanInitialLife ?: DefaultValue.humanInitialLife,
      oniInitialLife = oniInitialLife ?: DefaultValue.oniInitialLife,
      hybridInitialLife = hybridInitialLife ?: DefaultValue.hybridInitialLife,
      breathInitial = breathInitial ?: DefaultValue.breathInitial,
      bloodInitial = bloodInitial ?: DefaultValue.bloodInitial,
      familyRoll = familyRoll ?: DefaultValue.familyRoll,
      abilityRoll = abilityRoll ?: DefaultValue.abilityRoll,
      prodigyRoll = prodigyRoll ?: DefaultValue.prodigyRoll,
      markRoll = markRoll ?: DefaultValue.markRoll,
      berserkRoll = berserkRoll ?: DefaultValue.berserkRoll,
      rollCategoryId = rollCategoryId,
      offCategoryId = offCategoryId
    )
  }
  fun updateGuild(
    id: String,
    humanInitialLife: BigDecimal?,
    oniInitialLife: BigDecimal?,
    hybridInitialLife: BigDecimal?,
    breathInitial: BigDecimal?,
    bloodInitial: BigDecimal?,
    familyRoll: BigDecimal?,
    abilityRoll: BigDecimal?,
    prodigyRoll: BigDecimal?,
    markRoll: BigDecimal?,
    berserkRoll: BigDecimal?,
    rollCategoryId: String?,
    offCategoryId: String?
  ) {
    guilds.update({
      guilds.id eq id
    }) {
      if (humanInitialLife != null) {
        it[this.human_initial_life] = humanInitialLife
      }
      if (oniInitialLife != null) {
        it[this.oni_initial_life] = oniInitialLife
      }
      if (hybridInitialLife != null) {
        it[this.hybrid_initial_life] = hybridInitialLife
      }
      if (breathInitial != null) {
        it[this.breath_initial] = breathInitial
      }
      if (bloodInitial != null) {
        it[this.blood_initial] = bloodInitial
      }
      if (familyRoll != null) {
        it[this.family_roll] = familyRoll
      }
      if (abilityRoll != null) {
        it[this.ability_roll] = abilityRoll
      }
      if (prodigyRoll != null) {
        it[this.prodigy_roll] = prodigyRoll
      }
      if (markRoll != null) {
        it[this.mark_roll] = markRoll
      }
      if (berserkRoll != null) {
        it[this.berserk_roll] = berserkRoll
      }
      if (rollCategoryId != null) {
        it[this.roll_category_id] = rollCategoryId
      }
      if (offCategoryId != null) {
        it[this.off_category_id] = offCategoryId
      }
    }
  }
}