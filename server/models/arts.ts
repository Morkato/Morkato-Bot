import type { PrismaClient } from '@prisma/client'

import { NotFoundError, AlreadyExistsError } from 'morkato/errors'

import { assert, schemas } from 'morkato/schemas/utils'
import { validate } from 'morkato/schemas'

import { strip } from 'morkato/utils/string'
import { created_at, uuid } from 'morkato/utils/uuid'

export type ArtType = "RESPIRATION" | "KEKKIJUTSU" | 'FIGHTING_STYLE'
export type Art = {
  name: string
  type: ArtType
  id: string

  exclude: boolean

  embed_title: string | null
  embed_description: string | null
  embed_url: string | null

  guild_id: string

  updated_at: number
}

export function checkIsArtUniqueByName(name: string, art: Art) {
  return strip(name, {
    ignore_accents: true,
    ignore_empty: true,
    case_insensitive: true,
    trim: true
  }) === strip(art.name, {
    ignore_accents: true,
    ignore_empty: true,
    case_insensitive: true,
    trim: true
  })
}

type ArtWhereParams = {
  guild_id?: string
  type?: ArtType
}

type ArtGetherParams = { guild_id: string, id: string }
type ArtCreateParams = { guild_id: string, data: Omit<Partial<Art> & Pick<Art, 'name' | 'type'>, 'guild_id' | 'id'> }
type ArtEditParams = { guild_id: string, id: string, data: Omit<Partial<Art>, 'guild_id' | 'id'> }
type ArtDeleteParams = ArtGetherParams

interface ArtMembers {
  where({ guild_id, type }: ArtWhereParams): Promise<Art[]>
  get({ guild_id, id }: ArtGetherParams): Promise<Art>
  create({ guild_id, data }: ArtCreateParams): Promise<Art>
  edit({ guild_id, id, data }: ArtEditParams): Promise<Art>
  del({ guild_id, id }: ArtDeleteParams): Promise<Art>
}

export default function Arts(db: PrismaClient['art']): ArtMembers {
  async function where({ guild_id, type }: ArtWhereParams): Promise<Art[]> {
    guild_id = !guild_id ? guild_id : assert(schemas.id, guild_id)
    type = !type ? type : assert(schemas.art_type, type)

    const arts = await db.findMany({
      where: { guild_id, type },
      orderBy: { id: 'asc' }
    })

    return arts.map(art => ({ ...art, exclude: art.exclude === 'true', updated_at: Number(art.updated_at) }));
  }

  async function get({ guild_id, id }: ArtGetherParams): Promise<Art> {
    guild_id = assert(schemas.id, guild_id)
    id = assert(schemas.id, id)

    const art = await db.findUnique({ where: { guild_id_id: { guild_id, id } } })

    if (!art) {
      throw new NotFoundError({
        message: `Erro: A arte com o ID: ${id} não existe no servidor: ${guild_id}.`
      })
    }

    return { ...art, exclude: art.exclude === 'true', updated_at: Number(art.updated_at) };
  }

  async function create({ guild_id, data }: ArtCreateParams): Promise<Art> {
    guild_id = assert(schemas.id, guild_id)

    const { name, type, ...rest } = validate(data, {
      name: 'required',
      art_type: 'required',

      exclude: 'optional',

      embed_title: 'optional',
      embed_description: 'optional',
      embed_url: 'optional'
    }) as Partial<Omit<Art, 'id' | 'guild_id' | 'updated_at'>> & Pick<Art, 'name' | 'type'>

    const arts = await where({ guild_id })

    const hasOtherArt = !!arts.find(art => checkIsArtUniqueByName(name, art))

    if (hasOtherArt) {
      throw new AlreadyExistsError({
        message: `Erro: A arte com o nome: ${name} e tipo: ${type} já existe no servidor: ${guild_id}.`
      })
    }

    const id = uuid()
    const updated_at = created_at(id)

    const art = await db.create({
      data: {
        ...rest,
        guild_id,
        name,
        type,
        id,
        updated_at,
        exclude: rest.exclude === undefined ? undefined : rest.exclude ? 'true' : 'false'
      }
    })

    return { ...art, exclude: art.exclude === 'true', updated_at: Number(art.updated_at) };
  }
  async function edit({ guild_id, id, data }: ArtEditParams): Promise<Art> {
    guild_id = assert(schemas.id, guild_id)
    id = assert(schemas.id, id)

    const { name, ...rest } = validate(data, {
      name: 'optional',
      art_type: 'optional',

      exclude: 'optional',

      embed_title: 'optional',
      embed_description: 'optional',
      embed_url: 'optional'
    }) as Partial<Omit<Art, 'id' | 'guild_id' | 'created_at' | 'updated_at'>>

    if (name) {
      const arts = await where({ guild_id })

      const hasOtherArt = !!arts.find(art => checkIsArtUniqueByName(name as string, art) && art.id !== id)

      if (hasOtherArt) {
        throw new AlreadyExistsError({
          message: `Erro: A arte com o nome: ${name} já existe no servidor: ${guild_id}.`
        })
      }
    }

    try {
      const art = await db.update({
        where: { guild_id_id: { guild_id, id } },
        data: {
          ...rest,
          name,
          exclude: rest.exclude === undefined ? undefined : rest.exclude ? 'true' : 'false',
          updated_at: Date.now(),
        }
      })

      return { ...art, exclude: art.exclude === 'true', updated_at: Number(art.updated_at) };
    } catch {
      throw new NotFoundError({
        message: `Erro: A arte com o ID: ${id} não existe no servidor: ${guild_id}.`
      })
    }
  }
  async function del({ guild_id, id }: ArtDeleteParams): Promise<Art> {
    guild_id = assert(schemas.id, guild_id)
    id = assert(schemas.id, id)

    try {
      const art = await db.delete({ where: { guild_id_id: { guild_id, id } } })

      return { ...art, exclude: art.exclude === 'true', updated_at: Number(art.updated_at) };
    } catch {
      throw new NotFoundError({
        message: `Erro: A arte com o ID: ${id} não existe no servidor: ${guild_id}.`
      })
    }
  }

  return { where, get, create, edit, del };
}