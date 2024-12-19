CREATE SEQUENCE "ability_snowflake_seq";
CREATE TABLE "abilities" (
  "name" name_type NOT NULL,
  "key" key_type NOT NULL,
  "id" id_type NOT NULL DEFAULT snowflake_id('ability_snowflake_seq'),
  "guild_id" discord_id_type NOT NULL,
  "percent" percent_type NOT NULL DEFAULT 0,
  "user_type" INTEGER NOT NULL DEFAULT 0,
  "description" description_type DEFAULT NULL,
  "banner" banner_type DEFAULT NULL
);

ALTER TABLE "abilities"
  ADD CONSTRAINT "ability.pkey" PRIMARY KEY ("guild_id","id");
ALTER TABLE "abilities"
  ADD CONSTRAINT "ability.key" UNIQUE ("guild_id","key");
ALTER TABLE "abilities"
  ADD CONSTRAINT "ability.guild" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id")
  ON DELETE RESTRICT
  ON UPDATE RESTRICT;