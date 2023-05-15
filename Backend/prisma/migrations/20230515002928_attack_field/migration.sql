/*
  Warnings:

  - The primary key for the `attacks` table will be changed. If it partially fails, the table could be left without primary key constraint.

*/
-- AlterTable
ALTER TABLE "attacks" DROP CONSTRAINT "attacks_pkey",
ADD CONSTRAINT "attacks_pkey" PRIMARY KEY ("name", "guild_id");

-- CreateTable
CREATE TABLE "attacks_fields" (
    "id" TEXT NOT NULL,
    "text" TEXT NOT NULL,
    "guild_id" TEXT NOT NULL,
    "attack_name" TEXT NOT NULL,
    "roles" TEXT[],
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "attacks_fields_pkey" PRIMARY KEY ("guild_id","id")
);

-- AddForeignKey
ALTER TABLE "attacks_fields" ADD CONSTRAINT "attacks_fields_attack_name_guild_id_fkey" FOREIGN KEY ("attack_name", "guild_id") REFERENCES "attacks"("name", "guild_id") ON DELETE RESTRICT ON UPDATE CASCADE;
