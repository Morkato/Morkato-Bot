-- AlterTable
ALTER TABLE "attacks" ADD COLUMN     "damage" INTEGER NOT NULL DEFAULT 3000,
ADD COLUMN     "required_roles" INTEGER NOT NULL DEFAULT 0,
ADD COLUMN     "roles" TEXT[] DEFAULT ARRAY[]::TEXT[],
ADD COLUMN     "stamina" INTEGER NOT NULL DEFAULT 3000;