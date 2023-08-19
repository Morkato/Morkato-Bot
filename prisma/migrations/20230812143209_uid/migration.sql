/*
  Warnings:

  - The primary key for the `arts` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `key` on the `arts` table. All the data in the column will be lost.
  - You are about to drop the column `role` on the `arts` table. All the data in the column will be lost.
  - The primary key for the `attacks` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `art_key` on the `attacks` table. All the data in the column will be lost.
  - You are about to drop the column `damage` on the `attacks` table. All the data in the column will be lost.
  - You are about to drop the column `key` on the `attacks` table. All the data in the column will be lost.
  - You are about to drop the column `parent_key` on the `attacks` table. All the data in the column will be lost.
  - You are about to drop the column `required_roles` on the `attacks` table. All the data in the column will be lost.
  - You are about to drop the column `roles` on the `attacks` table. All the data in the column will be lost.
  - You are about to drop the column `stamina` on the `attacks` table. All the data in the column will be lost.
  - You are about to drop the `guild_variables` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropForeignKey
ALTER TABLE "attacks" DROP CONSTRAINT "attacks_art_key_guild_id_fkey";

-- DropForeignKey
ALTER TABLE "attacks" DROP CONSTRAINT "attacks_parent_key_guild_id_fkey";

-- DropForeignKey
ALTER TABLE "guild_variables" DROP CONSTRAINT "guild_variables_guild_id_fkey";

-- AlterTable
ALTER TABLE "arts" DROP CONSTRAINT "arts_pkey",
DROP COLUMN "key",
DROP COLUMN "role",
ADD COLUMN     "id" SERIAL NOT NULL,
ADD CONSTRAINT "arts_pkey" PRIMARY KEY ("id", "guild_id");

-- AlterTable
ALTER TABLE "attacks" DROP CONSTRAINT "attacks_pkey",
DROP COLUMN "art_key",
DROP COLUMN "damage",
DROP COLUMN "key",
DROP COLUMN "parent_key",
DROP COLUMN "required_roles",
DROP COLUMN "roles",
DROP COLUMN "stamina",
ADD COLUMN     "art_id" INTEGER,
ADD COLUMN     "id" SERIAL NOT NULL,
ADD COLUMN     "parent_id" INTEGER,
ADD CONSTRAINT "attacks_pkey" PRIMARY KEY ("id", "guild_id");

-- DropTable
DROP TABLE "guild_variables";

-- CreateTable
CREATE TABLE "variables" (
    "guild_id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "text" TEXT NOT NULL,
    "required_roles" INTEGER NOT NULL DEFAULT 1,
    "roles" TEXT[],
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "variables_pkey" PRIMARY KEY ("guild_id","name")
);

-- AddForeignKey
ALTER TABLE "attacks" ADD CONSTRAINT "attacks_art_id_guild_id_fkey" FOREIGN KEY ("art_id", "guild_id") REFERENCES "arts"("id", "guild_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "attacks" ADD CONSTRAINT "attacks_parent_id_guild_id_fkey" FOREIGN KEY ("parent_id", "guild_id") REFERENCES "attacks"("id", "guild_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "variables" ADD CONSTRAINT "variables_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE CASCADE ON UPDATE CASCADE;
