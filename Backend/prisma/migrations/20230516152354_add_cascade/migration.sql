-- DropForeignKey
ALTER TABLE "arts" DROP CONSTRAINT "arts_guild_id_fkey";

-- DropForeignKey
ALTER TABLE "attacks" DROP CONSTRAINT "attacks_art_name_guild_id_fkey";

-- DropForeignKey
ALTER TABLE "attacks_fields" DROP CONSTRAINT "attacks_fields_attack_name_guild_id_fkey";

-- AddForeignKey
ALTER TABLE "arts" ADD CONSTRAINT "arts_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guilds"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "attacks" ADD CONSTRAINT "attacks_art_name_guild_id_fkey" FOREIGN KEY ("art_name", "guild_id") REFERENCES "arts"("name", "guild_id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "attacks_fields" ADD CONSTRAINT "attacks_fields_attack_name_guild_id_fkey" FOREIGN KEY ("attack_name", "guild_id") REFERENCES "attacks"("name", "guild_id") ON DELETE CASCADE ON UPDATE CASCADE;
