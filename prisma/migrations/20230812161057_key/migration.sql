/*
  Warnings:

  - You are about to drop the column `key` on the `arts` table. All the data in the column will be lost.
  - You are about to drop the column `key` on the `attacks` table. All the data in the column will be lost.

*/
-- DropIndex
DROP INDEX "arts_key_key";

-- DropIndex
DROP INDEX "attacks_key_key";

-- AlterTable
ALTER TABLE "arts" DROP COLUMN "key";

-- AlterTable
ALTER TABLE "attacks" DROP COLUMN "key";
