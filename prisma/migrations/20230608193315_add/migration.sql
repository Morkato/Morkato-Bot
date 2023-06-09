/*
  Warnings:

  - You are about to drop the `attacks_fields` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `group_fields` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropForeignKey
ALTER TABLE "attacks" DROP CONSTRAINT "attacks_fields_key_guild_id_fkey";

-- DropForeignKey
ALTER TABLE "attacks_fields" DROP CONSTRAINT "attacks_fields_group_key_guild_id_fkey";

-- DropForeignKey
ALTER TABLE "attacks_fields" DROP CONSTRAINT "attacks_fields_guild_id_fkey";

-- DropForeignKey
ALTER TABLE "group_fields" DROP CONSTRAINT "group_fields_guild_id_fkey";

-- DropTable
DROP TABLE "attacks_fields";

-- DropTable
DROP TABLE "group_fields";

-- CreateTable
CREATE TABLE "guild_varialbles" (
    "guild_id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "text" TEXT NOT NULL,
    "visibleCaseIfNotPermitedMember" BOOLEAN NOT NULL DEFAULT false,
    "required_roles" INTEGER NOT NULL DEFAULT 1,
    "roles" TEXT[],
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "guild_varialbles_pkey" PRIMARY KEY ("guild_id","name")
);

-- AddForeignKey
ALTER TABLE "guild_varialbles" ADD CONSTRAINT "guild_varialbles_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
