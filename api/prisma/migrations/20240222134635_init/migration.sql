-- CreateEnum
CREATE TYPE "Bool" AS ENUM ('true', 'false');

-- CreateEnum
CREATE TYPE "ArtType" AS ENUM ('RESPIRATION', 'KEKKIJUTSU', 'FIGHTING_STYLE');

-- CreateEnum
CREATE TYPE "PlayerBreed" AS ENUM ('HUMAN', 'ONI', 'HYBRID');

-- CreateTable
CREATE TABLE "guilds" (
    "id" TEXT NOT NULL,

    CONSTRAINT "guild_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "arts" (
    "key" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "id" TEXT NOT NULL,
    "type" "ArtType" NOT NULL,
    "guild_id" TEXT NOT NULL,
    "embed_title" TEXT,
    "embed_description" TEXT,
    "embed_url" TEXT,
    "exclude" "Bool" NOT NULL DEFAULT 'false',
    "created_by" TEXT,
    "updated_at" TIMESTAMP(3),

    CONSTRAINT "art_pkey" PRIMARY KEY ("guild_id","id")
);

-- CreateTable
CREATE TABLE "attacks" (
    "key" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "id" TEXT NOT NULL,
    "title" TEXT,
    "description" TEXT,
    "banner" TEXT,
    "guild_id" TEXT NOT NULL,
    "art_id" TEXT NOT NULL,
    "parent_id" TEXT,
    "damage" INTEGER NOT NULL DEFAULT 0,
    "breath" INTEGER NOT NULL DEFAULT 0,
    "blood" INTEGER NOT NULL DEFAULT 0,
    "exclude" "Bool" NOT NULL DEFAULT 'false',
    "intents" INTEGER NOT NULL DEFAULT 0,
    "embed_title" TEXT,
    "embed_description" TEXT,
    "embed_url" TEXT,
    "created_by" TEXT,
    "updated_at" TIMESTAMP(3),

    CONSTRAINT "attack_pkey" PRIMARY KEY ("guild_id","id")
);

-- CreateTable
CREATE TABLE "items" (
    "guild_id" TEXT NOT NULL,
    "id" TEXT NOT NULL,
    "key" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT,
    "stack" SMALLINT NOT NULL DEFAULT 1,
    "usable" "Bool" NOT NULL DEFAULT 'false',
    "equippable" SMALLINT NOT NULL DEFAULT 0,
    "embed_title" TEXT,
    "embed_description" TEXT,
    "embed_url" TEXT,
    "created_by" TEXT,
    "updated_at" TIMESTAMP(3),

    CONSTRAINT "item_pkey" PRIMARY KEY ("guild_id","id")
);

-- CreateTable
CREATE TABLE "players" (
    "name" TEXT NOT NULL,
    "surname" TEXT,
    "credibility" INTEGER NOT NULL DEFAULT 0,
    "history" TEXT,
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
    "appearance" TEXT,
    "banner" TEXT,
    "updated_at" TIMESTAMP(3),

    CONSTRAINT "player_pkey" PRIMARY KEY ("guild_id","id")
);

-- CreateTable
CREATE TABLE "player_arts" (
    "guild_id" TEXT NOT NULL,
    "player_id" TEXT NOT NULL,
    "art_id" TEXT NOT NULL,

    CONSTRAINT "player_arts_pkey" PRIMARY KEY ("guild_id","player_id","art_id")
);

-- CreateTable
CREATE TABLE "inventory" (
    "guild_id" TEXT NOT NULL,
    "item_id" TEXT NOT NULL,
    "player_id" TEXT NOT NULL,
    "stack" SMALLINT NOT NULL DEFAULT 1,
    "created_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "inventory_pkey" PRIMARY KEY ("guild_id","player_id","item_id")
);

-- CreateIndex
CREATE UNIQUE INDEX "art_key" ON "arts"("guild_id", "key");

-- CreateIndex
CREATE UNIQUE INDEX "attack_key" ON "attacks"("guild_id", "key");

-- CreateIndex
CREATE UNIQUE INDEX "item_key" ON "items"("guild_id", "key");

-- AddForeignKey
ALTER TABLE "arts" ADD CONSTRAINT "fkey.guild_id" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "attacks" ADD CONSTRAINT "fkey.guild_id" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "attacks" ADD CONSTRAINT "fkey.art_id" FOREIGN KEY ("art_id", "guild_id") REFERENCES "arts"("id", "guild_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "attacks" ADD CONSTRAINT "fkey.parent_id" FOREIGN KEY ("parent_id", "guild_id") REFERENCES "attacks"("id", "guild_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "items" ADD CONSTRAINT "fkey.guild_id" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "players" ADD CONSTRAINT "fkey.guild_id" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "player_arts" ADD CONSTRAINT "fkey.guild_id" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "player_arts" ADD CONSTRAINT "fkey.player_id" FOREIGN KEY ("guild_id", "player_id") REFERENCES "players"("guild_id", "id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "player_arts" ADD CONSTRAINT "fkey.art_id" FOREIGN KEY ("guild_id", "art_id") REFERENCES "arts"("guild_id", "id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "inventory" ADD CONSTRAINT "fkey.guild_id" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "inventory" ADD CONSTRAINT "fkey.player_id" FOREIGN KEY ("guild_id", "player_id") REFERENCES "players"("guild_id", "id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "inventory" ADD CONSTRAINT "fkey.item_id" FOREIGN KEY ("guild_id", "item_id") REFERENCES "items"("guild_id", "id") ON DELETE CASCADE ON UPDATE CASCADE;
