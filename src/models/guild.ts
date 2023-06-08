import type { PrismaClient } from '@prisma/client'

import { type Guild, assertGuild } from './validator/guild'

import { assert, schemas } from './validator/utils'

export default function Guilds(db: PrismaClient['guild']) {
  return {
    async getAll(): Promise<Guild[]> {
      const guilds = await db.findMany();

      return guilds;
    },
    async get(id: string): Promise<Guild> {
      assert(schemas.id.required(), id)
      
      const guild = await db.findUnique({ where: { id } })

      if(!guild) {
        return await db.create({ data: { id } });
      }

      return guild;
    },
    async getGuilds(rows_id: string[]): Promise<Guild[]> {
      assert(schemas.arrayId.required(), rows_id)

      const guilds = await db.findMany({ where: { id: { in: rows_id } } })

      return guilds;
    },
    async deleteGuild(guild: Guild): Promise<Guild> {
      assertGuild(guild)
    
      const { id } = guild
    
      guild = await db.delete({ where: { id } })

      return guild;
    }
  }
}

export { type Guild, Guilds };