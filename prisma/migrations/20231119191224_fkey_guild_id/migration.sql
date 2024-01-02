-- RenameForeignKey
ALTER TABLE "inventory" RENAME CONSTRAINT "pkey.guild" TO "fkey.guild_id";

-- RenameForeignKey
ALTER TABLE "players" RENAME CONSTRAINT "pkey.guild_p" TO "fkey.guild_id";
