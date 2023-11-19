import type { PrismaClient } from '@prisma/client'

import { assert, schemas } from 'morkato/schemas/utils'
import { validate } from 'morkato/schemas'

import { NotFoundError } from 'morkato/errors'

type PlayerBreed = 'HUMAN' | 'ONI' | 'HYBRID'
type PlayerItem = { item_id: string, stack: number }
type Player = {
  guild_id: string
  id: string
  breed: PlayerBreed

  inventory: PlayerItem[]

  name: string
  credibility: number
  history: string | null

  cash: number

  life: number
  blood: number
  breath: number
  exp: number
  force: number
  resistance: number
  velocity: number

  appearance: string | null
  banner: string | null

  updated_at: number
}

type PlayerWhere = { guild_id?: string }
type PlayerGether = { guild_id: string, id: string }
type PlayerCreate = PlayerGether & { data: Omit<Partial<Player> & Pick<Player, 'name' | 'breed'>, 'guild_id' | 'id'> }
type PlayerEdit = PlayerGether & { data: Partial<Player> }
type PlayerDelete = PlayerGether
type PlayerAddItem = PlayerGether & { item_id: string, amount?: number }

export default function Players(db: PrismaClient['player'], playerItems: PrismaClient['playerItem']) {
  async function where({ guild_id }: PlayerWhere): Promise<Player[]> {
    if (guild_id) {
      guild_id = assert(schemas.id, guild_id)
    }

    const players = await db.findMany({
      where: { guild_id },
      include: {
        inventory: {
          select: {
            item_id: true,
            stack: true
          }
        }
      }
    })

    return players.map(player => ({ ...player, updated_at: Number(player.updated_at) }));
  }

  async function get({ guild_id, id }: PlayerGether): Promise<Player> {
    guild_id = assert(schemas.id, guild_id)
    id = assert(schemas.id, id)

    const player = await db.findUnique({
      where: { guild_id_id: { guild_id, id } },
      include: {
        inventory: {
          select: {
            item_id: true,
            stack: true
          }
        }
      }
    })

    if (!player) {
      throw new NotFoundError({
        message: `Erro: O player com o ID: ${id} não existe no servidor: ${guild_id}.`
      })
    }

    return { ...player, updated_at: Number(player.updated_at) };
  }

  async function create({ guild_id, id, data }: PlayerCreate): Promise<Player> {
    guild_id = assert(schemas.id, guild_id)
    id = assert(schemas.id, id)

    const { name, breed, ...rest } = validate(data, {
      name: 'required',
      breed: 'required',
      history: 'optional',

      cash: 'optional',

      life: 'optional',
      blood: 'optional',
      breath: 'optional',
      exp: 'optional',
      force: 'optional',
      resistance: 'optional',
      velocity: 'optional',

      appearance: 'optional',
      banner: 'optional'
    })

    try {
      const player = await db.create({
        data: { ...rest, guild_id, id, name, breed },
        include: {
          inventory: {
            select: {
              item_id: true,
              stack: true
            }
          }
        }
      })

      return { ...player, updated_at: Number(player.updated_at) };
    } catch {
      throw new NotFoundError({
        message: `Erro: O player com o ID: ${id} não existe no servidor: ${guild_id}.`
      })
    }
  }

  async function edit({ guild_id, id, data }: PlayerEdit): Promise<Player> {
    guild_id = assert(schemas.id, guild_id)
    id = assert(schemas.id, id)

    const rest = validate(data, {
      name: 'optional',
      breed: 'optional',
      history: 'optional',

      cash: 'optional',

      life: 'optional',
      blood: 'optional',
      breath: 'optional',
      exp: 'optional',
      force: 'optional',
      resistance: 'optional',
      velocity: 'optional',

      appearance: 'optional',
      banner: 'optional'
    })

    const player = await db.update({
      where: { guild_id_id: { guild_id, id } },
      data: rest,
      include: {
        inventory: {
          select: {
            item_id: true,
            stack: true
          }
        }
      }
    })

    return { ...player, updated_at: Number(player.updated_at) };
  }

  async function del({ guild_id, id }: PlayerDelete): Promise<Player> {
    guild_id = assert(schemas.id, guild_id)
    id = assert(schemas.id, id)

    try {
      const player = await db.delete({
        where: { guild_id_id: { guild_id, id } },
        include: {
          inventory: {
            select: {
              item_id: true,
              stack: true
            }
          }
        }
      })

      return { ...player, updated_at: Number(player.updated_at) };
    } catch {
      throw new NotFoundError({
        message: `Erro: O player com o ID: ${id} não existe no servidor: ${guild_id}.`
      })
    }
  }

  async function add_item({ guild_id, id, item_id, amount = 1 }: PlayerAddItem): Promise<Player> {
    guild_id = assert(schemas.id, guild_id)
    item_id = assert(schemas.id, item_id)
    id = assert(schemas.id, id)

    const player = await get({ guild_id, id })

    const itemInInventory = player.inventory.find(iv => iv.item_id === item_id)

    if (itemInInventory) {
      await playerItems.update({
        where: { guild_id_player_id_item_id: { guild_id, player_id: player.id, item_id: item_id } },
        data: {
          stack: itemInInventory.stack + amount
        }
      })

      itemInInventory.stack += amount

      return player;
    }

    await playerItems.create({
      data: {
        guild_id,
        player_id: player.id,
        item_id: item_id,
        stack: amount,
        created_at: Date.now()
      }
    })

    player.inventory.push({ item_id: item_id, stack: amount })

    return player;
  }

  return { where, get, create, edit, del };
}

export { Players };

export type { Player, PlayerBreed };