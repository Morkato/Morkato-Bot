import type { Player as PrismaPlayer } from '@prisma/client'
import type { Player } from 'type:models/player'

export function format({
  name,
  surname,
  breed,
  cash,
  exp,
  credibility,
  history,
  guild_id,
  id,
  life,
  breath,
  blood,
  force,
  resistance,
  velocity,
  appearance,
  banner,
  updated_at
}: PrismaPlayer): Player {
  return {
    name: name,
    surname: surname,
    breed: breed,
    cash: cash,
    exp: exp,
    credibility: credibility,
    history: history,
    guild_id: guild_id,
    id: id,
    life: life,
    breath: breath,
    blood: blood,
    force: force,
    resistance: resistance,
    velocity: velocity,
    appearance: appearance,
    banner: banner,
    updated_at: updated_at === null ? null : updated_at.getTime()
  }
}