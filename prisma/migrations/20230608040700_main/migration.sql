-- CreateEnum
CREATE TYPE "ArtType" AS ENUM ('RESPIRATION', 'KEKKIJUTSU');

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
    "key" TEXT NOT NULL,
    "type" "ArtType" NOT NULL,
    "role" TEXT,
    "guild_id" TEXT NOT NULL,
    "embed_title" TEXT,
    "embed_description" TEXT,
    "embed_url" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "arts_pkey" PRIMARY KEY ("key","guild_id")
);

-- CreateTable
CREATE TABLE "attacks" (
    "name" TEXT NOT NULL,
    "key" TEXT NOT NULL,
    "art_key" TEXT NOT NULL,
    "guild_id" TEXT NOT NULL,
    "roles" TEXT[] DEFAULT ARRAY[]::TEXT[],
    "required_roles" INTEGER NOT NULL DEFAULT 0,
    "required_exp" INTEGER NOT NULL DEFAULT 0,
    "damage" INTEGER NOT NULL DEFAULT 3000,
    "stamina" INTEGER NOT NULL DEFAULT 3000,
    "embed_title" TEXT,
    "embed_description" TEXT,
    "embed_url" TEXT,
    "fields_key" TEXT,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "attacks_pkey" PRIMARY KEY ("key","guild_id")
);

-- CreateTable
CREATE TABLE "attacks_fields" (
    "name" TEXT NOT NULL,
    "guild_id" TEXT NOT NULL,
    "text" TEXT NOT NULL,
    "roles" TEXT[],
    "required_roles" INTEGER NOT NULL DEFAULT 1,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "group_key" TEXT,

    CONSTRAINT "attacks_fields_pkey" PRIMARY KEY ("guild_id","name")
);

-- CreateTable
CREATE TABLE "group_fields" (
    "name" TEXT NOT NULL,
    "key" TEXT NOT NULL,
    "attack_key" TEXT,
    "guild_id" TEXT NOT NULL,

    CONSTRAINT "group_fields_pkey" PRIMARY KEY ("guild_id","key")
);

-- AddForeignKey
ALTER TABLE "arts" ADD CONSTRAINT "arts_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "attacks" ADD CONSTRAINT "attacks_art_key_guild_id_fkey" FOREIGN KEY ("art_key", "guild_id") REFERENCES "arts"("key", "guild_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "attacks" ADD CONSTRAINT "attacks_fields_key_guild_id_fkey" FOREIGN KEY ("fields_key", "guild_id") REFERENCES "group_fields"("key", "guild_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "attacks_fields" ADD CONSTRAINT "attacks_fields_group_key_guild_id_fkey" FOREIGN KEY ("group_key", "guild_id") REFERENCES "group_fields"("key", "guild_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "attacks_fields" ADD CONSTRAINT "attacks_fields_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "group_fields" ADD CONSTRAINT "group_fields_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
