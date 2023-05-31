/*
  Warnings:

  - The values [ATTACK] on the enum `ArtType` will be removed. If these variants are still used in the database, this will fail.
  - The primary key for the `arts` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - The primary key for the `attacks` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `art_name` on the `attacks` table. All the data in the column will be lost.
  - You are about to drop the column `attack_name` on the `attacks_fields` table. All the data in the column will be lost.
  - Added the required column `key` to the `arts` table without a default value. This is not possible if the table is not empty.
  - Added the required column `art_key` to the `attacks` table without a default value. This is not possible if the table is not empty.
  - Added the required column `key` to the `attacks` table without a default value. This is not possible if the table is not empty.
  - Added the required column `attack_key` to the `attacks_fields` table without a default value. This is not possible if the table is not empty.

*/
-- AlterEnum
BEGIN;
CREATE TYPE "ArtType_new" AS ENUM ('RESPIRATION', 'KEKKIJUTSU');
ALTER TABLE "arts" ALTER COLUMN "type" DROP DEFAULT;
ALTER TABLE "arts" ALTER COLUMN "type" TYPE "ArtType_new" USING ("type"::text::"ArtType_new");
ALTER TYPE "ArtType" RENAME TO "ArtType_old";
ALTER TYPE "ArtType_new" RENAME TO "ArtType";
DROP TYPE "ArtType_old";
COMMIT;

-- DropForeignKey
ALTER TABLE "attacks" DROP CONSTRAINT "attacks_art_name_guild_id_fkey";

-- DropForeignKey
ALTER TABLE "attacks_fields" DROP CONSTRAINT "attacks_fields_attack_name_guild_id_fkey";

-- AlterTable
ALTER TABLE "arts" DROP CONSTRAINT "arts_pkey",
ADD COLUMN     "key" TEXT NOT NULL,
ALTER COLUMN "type" DROP DEFAULT,
ADD CONSTRAINT "arts_pkey" PRIMARY KEY ("key", "guild_id");

-- AlterTable
ALTER TABLE "attacks" DROP CONSTRAINT "attacks_pkey",
DROP COLUMN "art_name",
ADD COLUMN     "art_key" TEXT NOT NULL,
ADD COLUMN     "key" TEXT NOT NULL,
ADD CONSTRAINT "attacks_pkey" PRIMARY KEY ("key", "guild_id");

-- AlterTable
ALTER TABLE "attacks_fields" DROP COLUMN "attack_name",
ADD COLUMN     "attack_key" TEXT NOT NULL;

-- AddForeignKey
ALTER TABLE "attacks" ADD CONSTRAINT "attacks_art_key_guild_id_fkey" FOREIGN KEY ("art_key", "guild_id") REFERENCES "arts"("key", "guild_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "attacks_fields" ADD CONSTRAINT "attacks_fields_attack_key_guild_id_fkey" FOREIGN KEY ("attack_key", "guild_id") REFERENCES "attacks"("key", "guild_id") ON DELETE CASCADE ON UPDATE CASCADE;
