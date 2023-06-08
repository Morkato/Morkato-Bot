/*
  Warnings:

  - The primary key for the `attacks_fields` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `attack_key` on the `attacks_fields` table. All the data in the column will be lost.
  - You are about to drop the column `id` on the `attacks_fields` table. All the data in the column will be lost.
  - Added the required column `fields_key` to the `attacks` table without a default value. This is not possible if the table is not empty.
  - Added the required column `name` to the `attacks_fields` table without a default value. This is not possible if the table is not empty.

*/
-- DropForeignKey
ALTER TABLE "attacks_fields" DROP CONSTRAINT "attacks_fields_attack_key_guild_id_fkey";

-- DropIndex
DROP INDEX "unique_guild_and_role";

-- AlterTable
ALTER TABLE "attacks" ADD COLUMN     "fields_key" TEXT NOT NULL;

-- AlterTable
ALTER TABLE "attacks_fields" DROP CONSTRAINT "attacks_fields_pkey",
DROP COLUMN "attack_key",
DROP COLUMN "id",
ADD COLUMN     "group_key" TEXT,
ADD COLUMN     "name" TEXT NOT NULL,
ADD COLUMN     "required_roles" INTEGER NOT NULL DEFAULT 1,
ADD CONSTRAINT "attacks_fields_pkey" PRIMARY KEY ("guild_id", "name");

-- CreateTable
CREATE TABLE "group_fields" (
    "name" TEXT NOT NULL,
    "key" TEXT NOT NULL,
    "attack_key" TEXT,
    "guild_id" TEXT NOT NULL,

    CONSTRAINT "group_fields_pkey" PRIMARY KEY ("guild_id","key")
);

-- AddForeignKey
ALTER TABLE "attacks" ADD CONSTRAINT "attacks_fields_key_guild_id_fkey" FOREIGN KEY ("fields_key", "guild_id") REFERENCES "group_fields"("key", "guild_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "attacks_fields" ADD CONSTRAINT "attacks_fields_group_key_guild_id_fkey" FOREIGN KEY ("group_key", "guild_id") REFERENCES "group_fields"("key", "guild_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "attacks_fields" ADD CONSTRAINT "attacks_fields_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "group_fields" ADD CONSTRAINT "group_fields_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
