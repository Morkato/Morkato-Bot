import { PrismaClient } from '@prisma/client'

import { uuid } from 'morkato/utils/uuid'
import { NotFoundError, AlreadyExistsError } from 'morkato/errors'

import { assert, schemas } from 'morkato/schemas/utils'
import { validate } from 'morkato/schemas'

import { strip } from 'morkato/utils/string'

type ItemWhereParams = { guild_id?: string }
type ItemGetherParams = { guild_id: string, id: string }
type ItemCreateParams = { guild_id: string, data: Omit<Partial<Item> & Pick<Item, 'name'>, 'guild_id' | 'id'> }
type ItemEditParams = { guild_id: string, id: string, data: Omit<Partial<Item>, 'guild_id' | 'id'> }
type ItemDeleteParams = ItemGetherParams

export interface ItemsMembers {
  where({ guild_id }: ItemWhereParams): Promise<Item[]>
  get({ guild_id, id }: ItemGetherParams): Promise<Item>
  create({ guild_id, data }: ItemCreateParams): Promise<Item>
  edit({ guild_id, id, data }: ItemEditParams): Promise<{ before: Item, after: Item }>
  del({ guild_id, id }: ItemDeleteParams): Promise<Item>
}

export type Item = {
  guild_id: string
  id: string

  name: string

  stack: number
  usable: boolean

  embed_title: string | null
  embed_description: string | null
  embed_url: string | null

  updated_at: number
}

const fmt_name = (text: string) => strip(text, { ignore_accents: true, ignore_empty: true, case_insensitive: true, trim: true })

export default function Items(db: PrismaClient['item']): ItemsMembers {
  async function where({ guild_id }: ItemWhereParams): Promise<Item[]> {
    guild_id = !guild_id ? guild_id : assert(schemas.id, guild_id)

    const items = await db.findMany({ where: { guild_id } })

    return items.map(item => ({ ...item, usable: item.usable === 'true' ? true : false, updated_at: Number(item.updated_at) }))
  }

  async function get({ guild_id, id }: ItemGetherParams): Promise<Item> {
    guild_id = assert(schemas.id, guild_id)
    id = assert(schemas.id, id)

    const item = await db.findUnique({ where: { guild_id_id: { guild_id, id } } })

    if (!item) {
      throw new NotFoundError({ message: "Esse item não existe." });
    }

    return { ...item, usable: item.usable === 'true' ? true : false, updated_at: Number(item.updated_at) };
  }

  async function create({ guild_id, data }: ItemCreateParams): Promise<Item> {
    guild_id = assert(schemas.id, guild_id)

    const { name, ...rest } = validate(data, {
      name: 'required',

      stack: 'optional',
      usable: 'optional',

      embed_title: 'optional',
      embed_description: 'optional',
      embed_url: 'optional'
    }) as typeof data

    const items = await where({ guild_id })
    const otherItem = items.find(item => fmt_name(item.name) === fmt_name(name))

    if (otherItem) {
      throw new AlreadyExistsError({ message: "Esse item já existe." });
    }

    const usable = rest.usable === undefined ? undefined : rest.usable ? 'true' : 'false'
    const updated_at = Date.now()
    const id = uuid(updated_at)

    const item = await db.create({ data: { guild_id, id, updated_at, name, ...rest, usable } })

    return { ...item, usable: rest.usable ?? false, updated_at: Number(item.updated_at) };
  }

  async function edit({ guild_id, id, data }: ItemEditParams): Promise<{ before: Item, after: Item }> {
    guild_id = assert(schemas.id, guild_id)
    id = assert(schemas.id, id)

    data = validate(data, {
      name: 'optional',

      stack: 'optional',
      usable: 'optional',

      embed_title: 'optional',
      embed_description: 'optional',
      embed_url: 'optional'
    }) as typeof data

    const before = await get({ guild_id, id })

    if (data.name) {
      const items = await where({ guild_id })
      const otherItem = items.find(item => {
        return fmt_name(item.name) === fmt_name(data.name as string) && item.id !== id
      })

      if (otherItem) {
        throw new AlreadyExistsError({ message: "Esse item já existe." });
      }
    }

    const usable = data.usable === undefined ? undefined : data.usable ? 'true' : 'false'
    const updated_at = Date.now()

    const after = await db.update({ where: { guild_id_id: { guild_id, id } }, data: { ...data, usable, updated_at } })

    return { before, after: { ...after, usable: after.usable == 'true' ? true : false, updated_at: Number(after.updated_at) } };
  }
  async function del({ guild_id, id }: ItemDeleteParams): Promise<Item> {
    guild_id = assert(schemas.id, guild_id)
    id = assert(schemas.id, id)

    try {
      const item = await db.delete({ where: { guild_id_id: { guild_id, id } } })

      return { ...item, usable: item.usable === 'true' ? true : false, updated_at: Number(item.updated_at) };
    } catch {
      throw new NotFoundError({ message: "Esse item não existe." });
    }
  }

  return { where, get, create, edit, del };
}

export { Items };