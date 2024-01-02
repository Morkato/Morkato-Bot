-- AlterTable
ALTER TABLE "inventory" ADD COLUMN     "equipped" SMALLINT NOT NULL DEFAULT 0;

-- AlterTable
ALTER TABLE "items" ADD COLUMN     "equippable" SMALLINT NOT NULL DEFAULT 0;
