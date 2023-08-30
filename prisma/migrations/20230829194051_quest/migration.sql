-- CreateTable
CREATE TABLE "quests" (
    "id" TEXT NOT NULL,
    "guild_id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "required_breed" "PlayerBreed",
    "allowed_channels" TEXT[],
    "required_exp" INTEGER NOT NULL,
    "title" TEXT,
    "description" TEXT,
    "url" TEXT NOT NULL,
    "icon" TEXT,
    "cooldown" INTEGER NOT NULL,

    CONSTRAINT "quests_pkey" PRIMARY KEY ("guild_id","id")
);

-- AddForeignKey
ALTER TABLE "quests" ADD CONSTRAINT "quests_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE CASCADE ON UPDATE CASCADE;
