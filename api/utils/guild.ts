import type { Guild as PrismaGuild } from '@prisma/client'
import type { Guild } from 'type:models/guild'

export function format({
  id
}: PrismaGuild): Guild {
  return { id };
}