/*
  Warnings:

  - The primary key for the `dialog_quests` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - A unique constraint covering the columns `[guild_id,quest_id,positon]` on the table `dialog_quests` will be added. If there are existing duplicate values, this will fail.
  - Added the required column `choose` to the `dialog_quests` table without a default value. This is not possible if the table is not empty.
  - Added the required column `positon` to the `dialog_quests` table without a default value. This is not possible if the table is not empty.

*/
-- CreateEnum
CREATE TYPE "DialogChoose" AS ENUM ('PLAYER', 'NPC');

-- AlterTable
ALTER TABLE "dialog_quests" DROP CONSTRAINT "dialog_quests_pkey",
ADD COLUMN     "choose" "DialogChoose" NOT NULL,
ADD COLUMN     "contents" TEXT[],
ADD COLUMN     "positon" INTEGER NOT NULL,
ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "id" SET DATA TYPE TEXT,
ADD CONSTRAINT "dialog_quests_pkey" PRIMARY KEY ("guild_id", "quest_id", "id");
DROP SEQUENCE "dialog_quests_id_seq";

-- CreateIndex
CREATE UNIQUE INDEX "dialog_quests_guild_id_quest_id_positon_key" ON "dialog_quests"("guild_id", "quest_id", "positon");
