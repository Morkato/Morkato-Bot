/*
  Warnings:

  - The primary key for the `arts` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - The primary key for the `attacks` table will be changed. If it partially fails, the table could be left without primary key constraint.

*/
-- DropForeignKey
ALTER TABLE "attacks" DROP CONSTRAINT "attacks_art_id_guild_id_fkey";

-- DropForeignKey
ALTER TABLE "attacks" DROP CONSTRAINT "attacks_parent_id_guild_id_fkey";

-- AlterTable
ALTER TABLE "arts" DROP CONSTRAINT "arts_pkey",
ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "id" SET DATA TYPE TEXT,
ADD CONSTRAINT "arts_pkey" PRIMARY KEY ("id", "guild_id");
DROP SEQUENCE "arts_id_seq";

-- AlterTable
ALTER TABLE "attacks" DROP CONSTRAINT "attacks_pkey",
ALTER COLUMN "art_id" SET DATA TYPE TEXT,
ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "id" SET DATA TYPE TEXT,
ALTER COLUMN "parent_id" SET DATA TYPE TEXT,
ADD CONSTRAINT "attacks_pkey" PRIMARY KEY ("id", "guild_id");
DROP SEQUENCE "attacks_id_seq";

-- AddForeignKey
ALTER TABLE "attacks" ADD CONSTRAINT "attacks_art_id_guild_id_fkey" FOREIGN KEY ("art_id", "guild_id") REFERENCES "arts"("id", "guild_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "attacks" ADD CONSTRAINT "attacks_parent_id_guild_id_fkey" FOREIGN KEY ("parent_id", "guild_id") REFERENCES "attacks"("id", "guild_id") ON DELETE RESTRICT ON UPDATE CASCADE;
