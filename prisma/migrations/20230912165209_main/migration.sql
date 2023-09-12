-- CreateEnum
CREATE TYPE "ArtType" AS ENUM ('RESPIRATION', 'KEKKIJUTSU', 'FIGHTING_STYLE');

-- CreateEnum
CREATE TYPE "PlayerBreed" AS ENUM ('HUMAN', 'ONI', 'HYBRID');

-- CreateEnum
CREATE TYPE "PlayerRank" AS ENUM ('F', 'E', 'D', 'C', 'B', 'A', 'AA', 'AAA', 'AAAA', 'S', 'SS', 'SSS', 'SSSS');

-- CreateEnum
CREATE TYPE "DialogChoose" AS ENUM ('PLAYER', 'NPC');

-- CreateTable
CREATE TABLE "guilds" (
    "id" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "guilds_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "arts" (
    "name" TEXT NOT NULL,
    "id" TEXT NOT NULL,
    "type" "ArtType" NOT NULL,
    "guild_id" TEXT NOT NULL,
    "embed_title" TEXT,
    "embed_description" TEXT,
    "embed_url" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "arts_pkey" PRIMARY KEY ("id","guild_id")
);

-- CreateTable
CREATE TABLE "attacks" (
    "name" TEXT NOT NULL,
    "id" TEXT NOT NULL,
    "guild_id" TEXT NOT NULL,
    "art_id" TEXT,
    "arm_id" TEXT,
    "parent_id" TEXT,
    "required_exp" INTEGER NOT NULL DEFAULT 0,
    "embed_title" TEXT,
    "embed_description" TEXT,
    "embed_url" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "armGuild_id" TEXT,
    "armId" TEXT,

    CONSTRAINT "attacks_pkey" PRIMARY KEY ("guild_id","id")
);

-- CreateTable
CREATE TABLE "players" (
    "name" TEXT NOT NULL,
    "credibility" INTEGER NOT NULL DEFAULT 0,
    "guild_id" TEXT NOT NULL,
    "id" TEXT NOT NULL,
    "breed" "PlayerBreed" NOT NULL,
    "cash" INTEGER NOT NULL DEFAULT 0,
    "rank" "PlayerRank" NOT NULL DEFAULT 'F',
    "life" INTEGER NOT NULL DEFAULT 0,
    "blood" INTEGER NOT NULL DEFAULT 0,
    "breath" INTEGER NOT NULL DEFAULT 0,
    "exp" INTEGER NOT NULL DEFAULT 0,
    "appearance" TEXT,

    CONSTRAINT "players_pkey" PRIMARY KEY ("guild_id","id")
);

-- CreateTable
CREATE TABLE "quests" (
    "id" TEXT NOT NULL,
    "guild_id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "required_breed" "PlayerBreed",
    "required_rank" "PlayerRank" NOT NULL,
    "allowed_channels" TEXT[],
    "required_exp" INTEGER NOT NULL,
    "title" TEXT,
    "description" TEXT,
    "url" TEXT,
    "icon" TEXT,

    CONSTRAINT "quests_pkey" PRIMARY KEY ("guild_id","id")
);

-- CreateTable
CREATE TABLE "dialog_quests" (
    "id" TEXT NOT NULL,
    "guild_id" TEXT NOT NULL,
    "quest_id" TEXT NOT NULL,
    "positon" INTEGER NOT NULL,
    "contents" TEXT[],
    "choose" "DialogChoose" NOT NULL,

    CONSTRAINT "dialog_quests_pkey" PRIMARY KEY ("guild_id","quest_id","id")
);

-- CreateTable
CREATE TABLE "arms" (
    "guild_id" TEXT NOT NULL,
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "role" TEXT,
    "embed_title" TEXT,
    "embed_description" TEXT,
    "embed_url" TEXT,

    CONSTRAINT "arms_pkey" PRIMARY KEY ("guild_id","id")
);

-- CreateIndex
CREATE UNIQUE INDEX "from_position" ON "dialog_quests"("guild_id", "quest_id", "positon");

-- AddForeignKey
ALTER TABLE "arts" ADD CONSTRAINT "arts_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "attacks" ADD CONSTRAINT "attacks_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "attacks" ADD CONSTRAINT "attacks_art_id_guild_id_fkey" FOREIGN KEY ("art_id", "guild_id") REFERENCES "arts"("id", "guild_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "attacks" ADD CONSTRAINT "attacks_parent_id_guild_id_fkey" FOREIGN KEY ("parent_id", "guild_id") REFERENCES "attacks"("id", "guild_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "attacks" ADD CONSTRAINT "attacks_armGuild_id_armId_fkey" FOREIGN KEY ("armGuild_id", "armId") REFERENCES "arms"("guild_id", "id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "players" ADD CONSTRAINT "players_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "quests" ADD CONSTRAINT "quests_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "dialog_quests" ADD CONSTRAINT "dialog_quests_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "dialog_quests" ADD CONSTRAINT "dialog_quests_guild_id_quest_id_fkey" FOREIGN KEY ("guild_id", "quest_id") REFERENCES "quests"("guild_id", "id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "arms" ADD CONSTRAINT "arms_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE CASCADE ON UPDATE CASCADE;
