/*
  Warnings:

  - Added the required column `required_rank` to the `quests` table without a default value. This is not possible if the table is not empty.

*/
-- CreateEnum
CREATE TYPE "PlayerRank" AS ENUM ('F', 'E', 'D', 'B', 'A', 'AA', 'AAA', 'AAAA', 'S', 'SS', 'SSS', 'SSSS');

-- AlterTable
ALTER TABLE "players" ADD COLUMN     "rank" "PlayerRank" NOT NULL DEFAULT 'F';

-- AlterTable
ALTER TABLE "quests" ADD COLUMN     "required_rank" "PlayerRank" NOT NULL;

-- CreateTable
CREATE TABLE "dialog_quests" (
    "id" SERIAL NOT NULL,
    "guild_id" TEXT NOT NULL,
    "quest_id" TEXT NOT NULL,

    CONSTRAINT "dialog_quests_pkey" PRIMARY KEY ("guild_id","quest_id","id")
);

-- AddForeignKey
ALTER TABLE "dialog_quests" ADD CONSTRAINT "dialog_quests_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "dialog_quests" ADD CONSTRAINT "dialog_quests_guild_id_quest_id_fkey" FOREIGN KEY ("guild_id", "quest_id") REFERENCES "quests"("guild_id", "id") ON DELETE CASCADE ON UPDATE CASCADE;
