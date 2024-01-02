-- RenameForeignKey
ALTER TABLE "arts" RENAME CONSTRAINT "arts_guild_id_fkey" TO "fkey.guild_id";

-- RenameForeignKey
ALTER TABLE "attacks" RENAME CONSTRAINT "attacks_art_id_guild_id_fkey" TO "fkey.art_id";

-- RenameForeignKey
ALTER TABLE "attacks" RENAME CONSTRAINT "attacks_guild_id_fkey" TO "fkey.guild_id";

-- RenameForeignKey
ALTER TABLE "attacks" RENAME CONSTRAINT "attacks_guild_id_item_id_fkey" TO "fkey.item_id";

-- RenameForeignKey
ALTER TABLE "attacks" RENAME CONSTRAINT "attacks_parent_id_guild_id_fkey" TO "fkey.parent_id";

-- RenameForeignKey
ALTER TABLE "inventory" RENAME CONSTRAINT "inventory_guild_id_item_id_fkey" TO "fkey.item_id";

-- RenameForeignKey
ALTER TABLE "inventory" RENAME CONSTRAINT "inventory_guild_id_player_id_fkey" TO "fkey.player_id";

-- RenameForeignKey
ALTER TABLE "items" RENAME CONSTRAINT "items_guild_id_fkey" TO "fkey.guild_id";
