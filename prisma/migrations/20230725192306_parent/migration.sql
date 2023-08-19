-- AlterTable
ALTER TABLE "attacks" ADD COLUMN     "parent_key" TEXT;

-- AddForeignKey
ALTER TABLE "attacks" ADD CONSTRAINT "attacks_parent_key_guild_id_fkey" FOREIGN KEY ("parent_key", "guild_id") REFERENCES "attacks"("key", "guild_id") ON DELETE RESTRICT ON UPDATE CASCADE;
