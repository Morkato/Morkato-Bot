/*
  Warnings:

  - Added the required column `credibility` to the `players` table without a default value. This is not possible if the table is not empty.
  - Added the required column `name` to the `players` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "players" ADD COLUMN     "credibility" INTEGER NOT NULL,
ADD COLUMN     "name" TEXT NOT NULL;
