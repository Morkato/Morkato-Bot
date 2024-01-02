-- AlterTable
ALTER TABLE "arts" ALTER COLUMN "updated_at" DROP NOT NULL;

-- AlterTable
ALTER TABLE "attacks" ALTER COLUMN "updated_at" DROP NOT NULL;

-- AlterTable
ALTER TABLE "items" ALTER COLUMN "updated_at" DROP NOT NULL;

-- AlterTable
ALTER TABLE "players" ALTER COLUMN "updated_at" DROP NOT NULL;
