-- CreateEnum
CREATE TYPE "ArtType" AS ENUM ('ATTACK', 'RESPIRATION', 'KEKKIJUTSU');

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
    "type" "ArtType" NOT NULL DEFAULT 'ATTACK',
    "role" TEXT,
    "guild_id" TEXT NOT NULL,
    "embed_title" TEXT,
    "embed_description" TEXT,
    "embed_url" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "arts_pkey" PRIMARY KEY ("name","guild_id")
);

-- CreateTable
CREATE TABLE "attacks" (
    "name" TEXT NOT NULL,
    "art_name" TEXT NOT NULL,
    "guild_id" TEXT NOT NULL,
    "roles" TEXT[] DEFAULT ARRAY[]::TEXT[],
    "required_roles" INTEGER NOT NULL DEFAULT 0,
    "damage" INTEGER NOT NULL DEFAULT 3000,
    "stamina" INTEGER NOT NULL DEFAULT 3000,
    "embed_title" TEXT,
    "embed_description" TEXT,
    "embed_url" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "attacks_pkey" PRIMARY KEY ("name","guild_id")
);

-- CreateTable
CREATE TABLE "attacks_fields" (
    "id" TEXT NOT NULL,
    "text" TEXT NOT NULL,
    "guild_id" TEXT NOT NULL,
    "attack_name" TEXT NOT NULL,
    "roles" TEXT[],
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "attacks_fields_pkey" PRIMARY KEY ("guild_id","id")
);

-- CreateIndex
CREATE INDEX "unique_guild_and_role" ON "arts"("role", "guild_id");

-- AddForeignKey
ALTER TABLE "arts" ADD CONSTRAINT "arts_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "attacks" ADD CONSTRAINT "attacks_art_name_guild_id_fkey" FOREIGN KEY ("art_name", "guild_id") REFERENCES "arts"("name", "guild_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "attacks_fields" ADD CONSTRAINT "attacks_fields_attack_name_guild_id_fkey" FOREIGN KEY ("attack_name", "guild_id") REFERENCES "attacks"("name", "guild_id") ON DELETE CASCADE ON UPDATE CASCADE;
