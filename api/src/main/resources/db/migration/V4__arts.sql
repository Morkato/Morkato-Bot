-- V3 CREATE TABLE ARTS
CREATE SEQUENCE "art_snowflake_seq";
CREATE TABLE "arts"(
  "name" name_type NOT NULL,
  "key" key_type NOT NULL,
  "guild_id" discord_id_type NOT NULL,
  "id" id_type NOT NULL DEFAULT snowflake_id('art_snowflake_seq'),
  "type" art_type NOT NULL,
  "energy" attr_type NOT NULL DEFAULT 25,
  "life" attr_type NOT NULL DEFAULT 1,
  "breath" attr_type NOT NULL DEFAULT 1,
  "blood" attr_type NOT NULL DEFAULT 1,
  "description" description_type DEFAULT NULL,
  "banner" banner_type DEFAULT NULL
);
ALTER TABLE "arts"
  ADD CONSTRAINT "art.pkey" PRIMARY KEY ("guild_id","id");
ALTER TABLE "arts"
  ADD CONSTRAINT "art.key" UNIQUE ("guild_id","key");
ALTER TABLE "arts"
  ADD CONSTRAINT "art.guild" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id")
  ON DELETE RESTRICT
  ON UPDATE RESTRICT;

CREATE INDEX "art_index_pkey" ON "arts"("guild_id","id");