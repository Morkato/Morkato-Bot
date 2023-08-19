/*
  Warnings:

  - A unique constraint covering the columns `[key]` on the table `arts` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[key]` on the table `attacks` will be added. If there are existing duplicate values, this will fail.
  - Added the required column `key` to the `arts` table without a default value. This is not possible if the table is not empty.
  - Added the required column `key` to the `attacks` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "arts" ADD COLUMN     "key" TEXT NOT NULL;

-- AlterTable
ALTER TABLE "attacks" ADD COLUMN     "key" TEXT NOT NULL;

-- CreateIndex
CREATE UNIQUE INDEX "arts_key_key" ON "arts"("key");

-- CreateIndex
CREATE UNIQUE INDEX "attacks_key_key" ON "attacks"("key");
