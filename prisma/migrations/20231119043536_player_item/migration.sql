/*
  Warnings:

  - You are about to alter the column `stack` on the `inventory` table. The data in that column could be lost. The data in that column will be cast from `Integer` to `SmallInt`.
  - You are about to alter the column `stack` on the `items` table. The data in that column could be lost. The data in that column will be cast from `Integer` to `SmallInt`.

*/
-- AlterTable
ALTER TABLE "inventory" ALTER COLUMN "stack" SET DATA TYPE SMALLINT;

-- AlterTable
ALTER TABLE "items" ALTER COLUMN "stack" SET DATA TYPE SMALLINT;
