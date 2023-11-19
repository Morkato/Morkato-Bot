import type { PrismaClient } from '@prisma/client'
import type { Player } from './players'
import type { Item } from './items'

import { assert, schemas } from 'morkato/schemas/utils'
import { validate } from 'morkato/schemas'
import { NotFoundError } from 'morkato/errors'

export type PlayerItem = {
  guild_id: string
  item_id: string
  player_id: string

  stack: number

  created_at: number
}

type PlayerItemWhere = { guild_id?: string, item_id?: string, player_id?: string }
type PlayerItemGather = { guild_id: string, item_id: string, player_id: string }
type PlayerItemCreate = { guild_id: string, item_id: string, player_id: string, data: Partial<Omit<PlayerItem, 'guild_id' | 'item_id' | 'player_id' | 'created_at'>> }
type PlayerItemEdit = PlayerItemCreate
type PlayerItemDel = PlayerItemGather

interface PlayerItemsMembers {
  where({ }: PlayerItemWhere): Promise<PlayerItem[]>
  get({ }: PlayerItemGather): Promise<PlayerItem>
  create({ }: PlayerItemCreate): Promise<PlayerItem>
  edit({ }: PlayerItemEdit): Promise<PlayerItem>
  del({ }: PlayerItemDel): Promise<PlayerItem>
}

export default function PlayerItem(db: PrismaClient['playerItem']): PlayerItemsMembers {
  async function where({ guild_id, item_id, player_id }: PlayerItemWhere): Promise<PlayerItem[]> {
    if (guild_id && item_id && player_id)
      return [await get({ guild_id, player_id, item_id }),];

    guild_id = !guild_id ? undefined : assert(schemas.id, guild_id)
    item_id = !item_id ? undefined : assert(schemas.id, item_id)
    player_id = !player_id ? undefined : assert(schemas.id, player_id)

    const playerItems = await db.findMany({ where: { guild_id, item_id, player_id } })

    return playerItems;
  }
  async function get({ guild_id, item_id, player_id }: PlayerItemGather): Promise<PlayerItem> {
    guild_id = assert(schemas.id, guild_id)
    item_id = assert(schemas.id, item_id)
    player_id = assert(schemas.id, player_id)

    const playerItem = await db.findUnique({ where: { guild_id_player_id_item_id: { guild_id, player_id, item_id } } })

    if (!playerItem) {
      throw new NotFoundError({ message: `O player: ${player_id} não tem o item: ${item_id}` })
    }

    return playerItem;
  }
  async function create({ guild_id, item_id, player_id, data }: PlayerItemCreate): Promise<PlayerItem> {
    guild_id = assert(schemas.id, guild_id)
    item_id = assert(schemas.id, item_id)
    player_id = assert(schemas.id, player_id)

    data = validate(data, {
      stack: 'optional'
    }) as typeof data

    const playerItem = await db.create({
      data: {
        ...data,
        guild_id,
        player_id,
        item_id,
        created_at: Date.now()
      }
    })

    return playerItem;
  }
  async function edit({ guild_id, item_id, player_id, data }: PlayerItemEdit): Promise<PlayerItem> {
    guild_id = assert(schemas.id, guild_id)
    item_id = assert(schemas.id, item_id)
    player_id = assert(schemas.id, player_id)

    data = validate(data, {
      stack: 'optional'
    }) as typeof data

    const playerItem = await db.update({
      where: { guild_id_player_id_item_id: { guild_id, player_id, item_id } },
      data: data
    })

    return playerItem;
  }
  async function del({ guild_id, item_id, player_id }: PlayerItemDel): Promise<PlayerItem> {
    guild_id = assert(schemas.id, guild_id)
    item_id = assert(schemas.id, item_id)
    player_id = assert(schemas.id, player_id)

    const playerItem = await db.delete({ where: { guild_id_player_id_item_id: { guild_id, player_id, item_id } } })

    return playerItem;
  }

  return { where, get, create, edit, del };
}