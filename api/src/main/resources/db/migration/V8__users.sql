CREATE TABLE "users" (
  "guild_id" discord_id_type NOT NULL,
  "id" discord_id_type NOT NULL,
  "type" user_type NOT NULL,
  "flags" INTEGER NOT NULL DEFAULT 0,
  "ability_roll" roll_type NOT NULL DEFAULT 3,
  "family_roll" roll_type NOT NULL DEFAULT 3,
  "prodigy_roll" roll_type NOT NULL DEFAULT 1,
  "mark_roll" roll_type NOT NULL DEFAULT 1,
  "berserk_roll" roll_type NOT NULL DEFAULT 1
);

ALTER TABLE "users"
  ADD CONSTRAINT "user.pkey" PRIMARY KEY ("guild_id","id");
ALTER TABLE "users"
  ADD CONSTRAINT "user.guild" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id")
  ON UPDATE RESTRICT
  ON DELETE RESTRICT;

CREATE TABLE "users_families" (
  "guild_id" discord_id_type NOT NULL,
  "user_id" discord_id_type NOT NULL,
  "family_id" id_type NOT NULL
);

ALTER TABLE "users_families"
  ADD CONSTRAINT "user_family.pkey" PRIMARY KEY ("guild_id","user_id","family_id");
ALTER TABLE "users_families"
  ADD CONSTRAINT "user_family.guild" FOREIGN KEY ("guild_id","family_id") REFERENCES "families"("guild_id","id");
ALTER TABLE "users_families"
  ADD CONSTRAINT "user_family.user" FOREIGN KEY ("guild_id","user_id") REFERENCES "users"("guild_id","id")
  ON DELETE CASCADE
  ON UPDATE RESTRICT;

CREATE TABLE "users_abilities" (
  "guild_id" discord_id_type NOT NULL,
  "user_id" discord_id_type NOT NULL,
  "ability_id" id_type NOT NULL
);

ALTER TABLE "users_abilities"
  ADD CONSTRAINT "user_ability.pkey" PRIMARY KEY ("guild_id","user_id","ability_id");
ALTER TABLE "users_abilities"
  ADD CONSTRAINT "user_ability.guild" FOREIGN KEY ("guild_id","ability_id") REFERENCES "abilities"("guild_id","id");
ALTER TABLE "users_abilities"
  ADD CONSTRAINT "user_ability.user" FOREIGN KEY ("guild_id","user_id") REFERENCES "users"("guild_id","id")
  ON DELETE CASCADE
  ON UPDATE RESTRICT;