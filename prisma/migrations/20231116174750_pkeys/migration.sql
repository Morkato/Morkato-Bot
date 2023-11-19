-- CreateEnum
CREATE TYPE "Bool" AS ENUM ('true', 'false');

-- CreateEnum
CREATE TYPE "ArtType" AS ENUM ('RESPIRATION', 'KEKKIJUTSU', 'FIGHTING_STYLE');

-- CreateEnum
CREATE TYPE "PlayerBreed" AS ENUM ('HUMAN', 'ONI', 'HYBRID');

-- CreateEnum
CREATE TYPE "DialogChoose" AS ENUM ('PLAYER', 'NPC');

-- CreateTable
CREATE TABLE "guilds" (
    "id" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "guild_pkey" PRIMARY KEY ("id")
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
    "exclude" "Bool" NOT NULL DEFAULT 'false',
    "updated_at" INTEGER NOT NULL,

    CONSTRAINT "art_pkey" PRIMARY KEY ("guild_id","id")
);

-- CreateTable
CREATE TABLE "attacks" (
    "name" TEXT NOT NULL,
    "id" TEXT NOT NULL,
    "guild_id" TEXT NOT NULL,
    "art_id" TEXT,
    "item_id" TEXT,
    "parent_id" TEXT,
    "required_exp" INTEGER NOT NULL DEFAULT 0,
    "damage" INTEGER NOT NULL DEFAULT 0,
    "breath" INTEGER NOT NULL DEFAULT 0,
    "blood" INTEGER NOT NULL DEFAULT 0,
    "exclude" "Bool" NOT NULL DEFAULT 'false',
    "embed_title" TEXT,
    "embed_description" TEXT,
    "embed_url" TEXT,
    "updated_at" INTEGER NOT NULL,

    CONSTRAINT "attack_pkey" PRIMARY KEY ("guild_id","id")
);

-- CreateTable
CREATE TABLE "players" (
    "name" TEXT NOT NULL,
    "credibility" INTEGER NOT NULL DEFAULT 0,
    "history" TEXT,
    "mission" INTEGER,
    "guild_id" TEXT NOT NULL,
    "id" TEXT NOT NULL,
    "breed" "PlayerBreed" NOT NULL,
    "cash" INTEGER NOT NULL DEFAULT 0,
    "life" INTEGER NOT NULL DEFAULT 0,
    "blood" INTEGER NOT NULL DEFAULT 0,
    "breath" INTEGER NOT NULL DEFAULT 0,
    "exp" INTEGER NOT NULL DEFAULT 0,
    "force" INTEGER NOT NULL DEFAULT 0,
    "resistance" INTEGER NOT NULL DEFAULT 0,
    "velocity" INTEGER NOT NULL DEFAULT 1,
    "reflex" INTEGER NOT NULL DEFAULT 1,
    "appearance" TEXT,
    "banner" TEXT,
    "updated_at" INTEGER NOT NULL,

    CONSTRAINT "player_pkey" PRIMARY KEY ("guild_id","id")
);

-- CreateTable
CREATE TABLE "items" (
    "guild_id" TEXT NOT NULL,
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "stack" INTEGER NOT NULL DEFAULT 1,
    "usable" "Bool" NOT NULL DEFAULT 'false',
    "embed_title" TEXT,
    "embed_description" TEXT,
    "embed_url" TEXT,
    "updated_at" INTEGER NOT NULL,

    CONSTRAINT "item_pkey" PRIMARY KEY ("guild_id","id")
);

-- AddForeignKey
ALTER TABLE "arts" ADD CONSTRAINT "arts_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "attacks" ADD CONSTRAINT "attacks_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "attacks" ADD CONSTRAINT "attacks_art_id_guild_id_fkey" FOREIGN KEY ("art_id", "guild_id") REFERENCES "arts"("id", "guild_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "attacks" ADD CONSTRAINT "attacks_guild_id_item_id_fkey" FOREIGN KEY ("guild_id", "item_id") REFERENCES "items"("guild_id", "id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "attacks" ADD CONSTRAINT "attacks_parent_id_guild_id_fkey" FOREIGN KEY ("parent_id", "guild_id") REFERENCES "attacks"("id", "guild_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "players" ADD CONSTRAINT "players_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "items" ADD CONSTRAINT "items_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE CASCADE ON UPDATE CASCADE;
