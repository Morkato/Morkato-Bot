import type { Guild as PrismaGuild } from '@prisma/client'
import type { Guild } from 'type:models/guild'

export function format({
  id,
  created_at,
  updated_at
}: PrismaGuild): Guild {
  return { id, created_at, updated_at };
}