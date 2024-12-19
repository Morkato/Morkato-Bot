CREATE SEQUENCE "family_snowflake_seq";
CREATE TABLE "families" (
  "name" name_type NOT NULL,
  "key" key_type NOT NULL,
  "id" id_type NOT NULL DEFAULT snowflake_id('family_snowflake_seq'),
  "guild_id" discord_id_type NOT NULL,
  "percent" percent_type NOT NULL DEFAULT 0,
  "user_type" INTEGER NOT NULL DEFAULT 0,
  "description" description_type DEFAULT NULL,
  "banner" banner_type DEFAULT NULL
);

ALTER TABLE "families"
  ADD CONSTRAINT "family.pkey" PRIMARY KEY ("guild_id","id");
ALTER TABLE "families"
  ADD CONSTRAINT "family.key" UNIQUE ("guild_id","key");
ALTER TABLE "families"
  ADD CONSTRAINT "family.guild" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id")
  ON DELETE RESTRICT
  ON UPDATE RESTRICT;