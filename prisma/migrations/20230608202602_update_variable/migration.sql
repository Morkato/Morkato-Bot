/*
  Warnings:

  - You are about to drop the column `visibleCaseIfNotPermitedMember` on the `guild_varialbles` table. All the data in the column will be lost.

*/
-- AlterTable
ALTER TABLE "guild_varialbles" DROP COLUMN "visibleCaseIfNotPermitedMember",
ADD COLUMN     "visibleCaseIfNotAuthorizerMember" BOOLEAN NOT NULL DEFAULT false;
