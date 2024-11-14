CREATE SEQUENCE "ability_snowflake_seq";
CREATE TABLE "abilities" (
  "name" name_type NOT NULL,
  "key" key_type NOT NULL,
  "id" id_type NOT NULL DEFAULT snowflake_id('ability_snowflake_seq'),
  "energy" energy_type NOT NULL,
  "guild_id" discord_id_type NOT NULL,
  "percent" percent_type NOT NULL DEFAULT 0,
  "npc_type" INTEGER NOT NULL,
  "description" description_type DEFAULT NULL,
  "banner" banner_type DEFAULT NULL
);

CREATE SEQUENCE "family_snowflake_seq";
CREATE TABLE "families" (
  "name" name_type NOT NULL,
  "key" key_type NOT NULL,
  "id" id_type NOT NULL DEFAULT snowflake_id('family_snowflake_seq'),
  "guild_id" discord_id_type NOT NULL,
  "percent" percent_type NOT NULL DEFAULT 0,
  "npc_type" INTEGER NOT NULL,
  "description" description_type DEFAULT NULL,
  "banner" banner_type DEFAULT NULL
);

CREATE TABLE "abilities_families" (
  "ability_id" id_type NOT NULL,
  "family_id" id_type NOT NULL,
  "guild_id" discord_id_type NOT NULL
);

ALTER TABLE "families"
  ADD CONSTRAINT "family.pkey" PRIMARY KEY ("guild_id","id");
ALTER TABLE "families"
  ADD CONSTRAINT "family.key" UNIQUE ("guild_id","key");
ALTER TABLE "families"
  ADD CONSTRAINT "family.guild" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id")
  ON DELETE RESTRICT
  ON UPDATE RESTRICT;

ALTER TABLE "abilities"
  ADD CONSTRAINT "ability.pkey" PRIMARY KEY ("guild_id", "id");
ALTER TABLE "abilities"
  ADD CONSTRAINT "ability.key" UNIQUE ("guild_id","key");
ALTER TABLE "abilities"
  ADD CONSTRAINT "ability.guild" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id")
  ON DELETE RESTRICT
  ON UPDATE RESTRICT;

ALTER TABLE "abilities_families"
  ADD CONSTRAINT "ability_family.pkey" PRIMARY KEY ("guild_id","family_id","ability_id");
ALTER TABLE "abilities_families"
  ADD CONSTRAINT "ability_family.ability" FOREIGN KEY ("guild_id","ability_id") REFERENCES "abilities"("guild_id","id")
  ON DELETE CASCADE
  ON UPDATE RESTRICT;
ALTER TABLE "abilities_families"
  ADD CONSTRAINT "ability_family.family" FOREIGN KEY ("guild_id","family_id") REFERENCES "families"("guild_id","id")
  ON DELETE CASCADE
  ON UPDATE RESTRICT;

CREATE INDEX "ability_index_pkey" ON "abilities"("guild_id","id");
CREATE INDEX "family_index_pkey" ON "families"("guild_id","id");