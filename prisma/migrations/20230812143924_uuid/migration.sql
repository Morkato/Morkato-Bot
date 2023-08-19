/*
  Warnings:

  - The primary key for the `arts` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - The `id` column on the `arts` table would be dropped and recreated. This will lead to data loss if there is data in the column.
  - The primary key for the `attacks` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - The `art_id` column on the `attacks` table would be dropped and recreated. This will lead to data loss if there is data in the column.
  - The `id` column on the `attacks` table would be dropped and recreated. This will lead to data loss if there is data in the column.
  - The `parent_id` column on the `attacks` table would be dropped and recreated. This will lead to data loss if there is data in the column.
  - You are about to drop the `variables` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropForeignKey
ALTER TABLE "attacks" DROP CONSTRAINT "attacks_art_id_guild_id_fkey";

-- DropForeignKey
ALTER TABLE "attacks" DROP CONSTRAINT "attacks_parent_id_guild_id_fkey";

-- DropForeignKey
ALTER TABLE "variables" DROP CONSTRAINT "variables_guild_id_fkey";

-- AlterTable
ALTER TABLE "arts" DROP CONSTRAINT "arts_pkey",
DROP COLUMN "id",
ADD COLUMN     "id" SERIAL NOT NULL,
ADD CONSTRAINT "arts_pkey" PRIMARY KEY ("id", "guild_id");

-- AlterTable
ALTER TABLE "attacks" DROP CONSTRAINT "attacks_pkey",
DROP COLUMN "art_id",
ADD COLUMN     "art_id" INTEGER,
DROP COLUMN "id",
ADD COLUMN     "id" SERIAL NOT NULL,
DROP COLUMN "parent_id",
ADD COLUMN     "parent_id" INTEGER,
ADD CONSTRAINT "attacks_pkey" PRIMARY KEY ("id", "guild_id");

-- DropTable
DROP TABLE "variables";

-- CreateTable
CREATE TABLE "guild_variables" (
    "guild_id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "text" TEXT NOT NULL,
    "required_roles" INTEGER NOT NULL DEFAULT 1,
    "roles" TEXT[],
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "guild_variables_pkey" PRIMARY KEY ("guild_id","name")
);

-- AddForeignKey
ALTER TABLE "attacks" ADD CONSTRAINT "attacks_art_id_guild_id_fkey" FOREIGN KEY ("art_id", "guild_id") REFERENCES "arts"("id", "guild_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "attacks" ADD CONSTRAINT "attacks_parent_id_guild_id_fkey" FOREIGN KEY ("parent_id", "guild_id") REFERENCES "attacks"("id", "guild_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "guild_variables" ADD CONSTRAINT "guild_variables_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE CASCADE ON UPDATE CASCADE;
