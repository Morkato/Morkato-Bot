/*
  Warnings:

  - Added the required column `created_at` to the `player_arts` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "player_arts" ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL;
