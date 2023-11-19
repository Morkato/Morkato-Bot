-- CreateTable
CREATE TABLE "inventory" (
    "guild_id" TEXT NOT NULL,
    "item_id" TEXT NOT NULL,
    "player_id" TEXT NOT NULL,
    "stack" INTEGER NOT NULL,
    "created_at" INTEGER NOT NULL,

    CONSTRAINT "inventory_pkey" PRIMARY KEY ("guild_id","player_id","item_id")
);

-- AddForeignKey
ALTER TABLE "inventory" ADD CONSTRAINT "inventory_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "inventory" ADD CONSTRAINT "inventory_guild_id_player_id_fkey" FOREIGN KEY ("guild_id", "player_id") REFERENCES "players"("guild_id", "id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "inventory" ADD CONSTRAINT "inventory_guild_id_item_id_fkey" FOREIGN KEY ("guild_id", "item_id") REFERENCES "items"("guild_id", "id") ON DELETE CASCADE ON UPDATE CASCADE;
