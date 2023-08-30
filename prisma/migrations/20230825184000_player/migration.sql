-- CreateEnum
CREATE TYPE "PlayerBreed" AS ENUM ('HUMAN', 'ONI', 'HYBRID');

-- CreateTable
CREATE TABLE "players" (
    "guild_id" TEXT NOT NULL,
    "id" TEXT NOT NULL,
    "breed" "PlayerBreed" NOT NULL,
    "cash" INTEGER NOT NULL DEFAULT 0,
    "life" INTEGER NOT NULL DEFAULT 0,
    "blood" INTEGER NOT NULL DEFAULT 0,
    "breath" INTEGER NOT NULL DEFAULT 0,
    "exp" INTEGER NOT NULL DEFAULT 0,
    "appearance" TEXT,

    CONSTRAINT "players_pkey" PRIMARY KEY ("guild_id","id")
);

-- AddForeignKey
ALTER TABLE "players" ADD CONSTRAINT "players_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE CASCADE ON UPDATE CASCADE;
