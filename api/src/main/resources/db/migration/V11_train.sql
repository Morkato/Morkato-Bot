CREATE SEQUENCE "trainer_snowflake_seq";
CREATE TABLE "trainers" (
  "guild_id" discord_id_type NOT NULL,
  "id" id_type NOT NULL DEFAULT snowflake_id('trainer_snowflake_seq'),
  "channel_id" discord_id_type NOT NULL,
  "name" name_type NOT NULL,
  "key" key_type NOT NULL,
  "xp" xp_train_map_type NOT NULL DEFAULT '{0,0,0,0}'::xp_train_map_type
  "description" description_type DEFAULT NULL,
  "banner" banner_type DEFAULT NULL
);