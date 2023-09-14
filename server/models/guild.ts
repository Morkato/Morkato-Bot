import type { Guild }                from './validator/guild'
import type { PrismaClient, Prisma } from '@prisma/client'

import { assert, schemas } from './validator/utils'

const select: Prisma.GuildSelect = {
  id: true,

  created_at: true,
  updated_at: true
}

export default function Guilds(db: PrismaClient['guild']) {
  return {
    async getAll(): Promise<Guild[]> {
      const guilds = await db.findMany({ select }) as Guild[];

      return guilds;
    },
    async get(id: string): Promise<Guild> {
      assert(schemas.id.required(), id)
      
      const guild = await db.findUnique({ where: { id }, select }) as Guild

      if(!guild) {
        return await db.create({ data: { id }, select }) as Guild;
      }

      return guild;
    },
    async getGuilds(rows_id: string[]): Promise<Guild[]> {
      assert(schemas.arrayId.required(), rows_id)

      const guilds = await db.findMany({ where: { id: { in: rows_id } } }) as Guild[]

      return guilds;
    },
    async deleteGuild(id: string): Promise<Guild> {
      assert(schemas.id.required(), id)

      return await db.delete({ where: { id }, select }) as Guild;
    }
  }
}

export { type Guild, Guilds };