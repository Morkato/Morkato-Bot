import type { PlayerArt as PrismaPlayerArt } from '@prisma/client'
import type { PlayerArt } from 'type:models/playerArt'

export function format({
  guild_id,
  player_id,
  art_id,
  created_at
}: PrismaPlayerArt): PlayerArt {
  return {
    guild_id: guild_id,
    player_id: player_id,
    art_id: art_id,
    created_at: created_at.getTime()
  }
}