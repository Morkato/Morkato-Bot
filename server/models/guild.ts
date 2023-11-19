import type { PrismaClient, Prisma } from '@prisma/client'

import { assert, schemas } from 'morkato/schemas/utils'

import {
  NotFoundError
} from 'morkato/errors'

export type Guild = {
  id: string

  created_at: Date
  updated_at: Date
}

const select: Prisma.GuildSelect = {
  id: true,

  created_at: true,
  updated_at: true
}

type WhereGuild = { ids?: string[] }

export default function Guilds(db: PrismaClient['guild']) {
  async function where({ ids }: WhereGuild): Promise<Guild[]> {
    if (ids) {
      assert(schemas.ids, ids)

      const guilds = await db.findMany({ where: { id: { in: ids } }, select }) as Guild[];

      return guilds;
    }

    const guilds = await db.findMany({ select }) as Guild[];

    return guilds;
  }

  async function get(id: string): Promise<Guild> {
    assert(schemas.id.required(), id)

    const guild = await db.findUnique({ where: { id }, select }) as Guild

    if (!guild) {
      throw new NotFoundError({
        message: `O servidor com o ID ${id} não está configurado.`
      })
    }

    return guild;
  }

  async function del(id: string): Promise<Guild> {
    assert(schemas.id.required(), id)

    try {
      return await db.delete({ where: { id }, select }) as Guild;
    } catch {
      throw new NotFoundError({
        message: `O servidor com o ID ${id} não está configurado.`
      })
    }
  }

  return { where, get, del };
}

export { Guilds };