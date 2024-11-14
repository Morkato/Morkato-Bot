--  // Flags: Flags do NPC.

--  // 0: Nenhuma
--  // (1 << 1): Prodígio
--  // (1 << 2): Marca
--  // (1 << 3): Berserk Mode
CREATE SEQUENCE "npc_snowflake_seq";
CREATE TABLE "npcs" (
  "name" name_type NOT NULL,
  "type" npc_type NOT NULL,
  "surname" surname_type NOT NULL,
  "guild_id" discord_id_type NOT NULL,
  "family_id" id_type NOT NULL,
  "id" id_type NOT NULL DEFAULT snowflake_id('npc_snowflake_seq'),
  "max_energy" energy_type NOT NULL DEFAULT 100,
  "energy" energy_type NOT NULL DEFAULT 100,
  "flags" INTEGER NOT NULL DEFAULT 0,
  "max_life" attr_type NOT NULL DEFAULT 0,
  "max_breath" attr_type NOT NULL DEFAULT 0,
  "max_blood" attr_type NOT NULL DEFAULT 0,
  "current_life" attr_type NOT NULL DEFAULT 0,
  "current_breath" attr_type NOT NULL DEFAULT 0,
  "current_blood" attr_type NOT NULL DEFAULT 0,
  "icon" banner_type DEFAULT NULL,
  "last_action" TIMESTAMP DEFAULT NULL
);

CREATE TABLE "npcs_abilities" (
  "guild_id" discord_id_type NOT NULL,
  "npc_id" id_type NOT NULL,
  "ability_id" id_type NOT NULL
);

CREATE TABLE "npcs_arts" (
  "guild_id" discord_id_type NOT NULL,
  "npc_id" id_type NOT NULL,
  "art_id" id_type NOT NULL,
  "exp" attr_type NOT NULL DEFAULT 0
);

ALTER TABLE "npcs"
  ADD CONSTRAINT "npc.pkey" PRIMARY KEY ("guild_id","id");
ALTER TABLE "npcs"
  ADD CONSTRAINT "npc.surname" UNIQUE ("guild_id", "surname");
ALTER TABLE "npcs"
  ADD CONSTRAINT "npc.guild" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id")
  ON DELETE RESTRICT
  ON UPDATE RESTRICT;
 ALTER TABLE "npcs"
   ADD CONSTRAINT "npc.family" FOREIGN KEY ("guild_id","family_id") REFERENCES "families"("guild_id","id")
   ON DELETE RESTRICT
   ON UPDATE RESTRICT;

ALTER TABLE "npcs"
  ADD CONSTRAINT "npc.current_life" CHECK ("max_life" >= "current_life");
ALTER TABLE "npcs"
  ADD CONSTRAINT "npc.current_breath" CHECK ("max_breath" >= "current_breath");
ALTER TABLE "npcs"
  ADD CONSTRAINT "npc.current_blood" CHECK ("max_blood" >= "current_blood");
ALTER TABLE "npcs"
  ADD CONSTRAINT "npc.energy" CHECK ("max_energy" >= "energy");

ALTER TABLE "npcs_abilities"
  ADD CONSTRAINT "npc_ability.pkey" PRIMARY KEY ("guild_id","npc_id","ability_id");
ALTER TABLE "npcs_abilities"
  ADD CONSTRAINT "npc_ability.ability" FOREIGN KEY ("guild_id","ability_id") REFERENCES "abilities"("guild_id","id")
  ON DELETE RESTRICT
  ON UPDATE RESTRICT;
ALTER TABLE "npcs_abilities"
  ADD CONSTRAINT "npc_ability.npc" FOREIGN KEY ("guild_id","npc_id") REFERENCES "npcs"("guild_id","id")
  ON DELETE CASCADE
  ON UPDATE RESTRICT;

ALTER TABLE "npcs_arts"
  ADD CONSTRAINT "npc_art.pkey" PRIMARY KEY ("guild_id","npc_id","art_id");
ALTER TABLE "npcs_arts"
  ADD CONSTRAINT "npc_art.npc" FOREIGN KEY ("guild_id","npc_id") REFERENCES "npcs"("guild_id","id")
  ON DELETE CASCADE
  ON UPDATE RESTRICT;
ALTER TABLE "npcs_arts"
  ADD CONSTRAINT "npc_art.art" FOREIGN KEY ("guild_id","art_id") REFERENCES "arts"("guild_id","id")
  ON DELETE RESTRICT
  ON UPDATE RESTRICT;

CREATE INDEX "npc_index_pkey" ON "npcs"("guild_id","id");