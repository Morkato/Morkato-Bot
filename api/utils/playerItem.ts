import type { PlayerItem as PrismaPlayerItem } from '@prisma/client'
import type { PlayerItem } from 'type:models/playerItem'

export function format({
  guild_id,
  player_id,
  item_id,
  stack,
  created_at
}: PrismaPlayerItem): PlayerItem {
  return {
    guild_id: guild_id,
    player_id: player_id,
    item_id: item_id,
    stack: stack,
    created_at: Number(created_at)
  };
}