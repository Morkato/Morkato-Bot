/*
  Warnings:

  - You are about to drop the column `equipped` on the `inventory` table. All the data in the column will be lost.
  - Added the required column `created_at` to the `inventory` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "inventory" DROP COLUMN "equipped",
ADD COLUMN     "created_at" BIGINT NOT NULL;
