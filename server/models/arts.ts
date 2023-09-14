import type { Art, ArtType } from './validator/art'
import type { PrismaClient } from '@prisma/client'

import { validate, id as schema_id, type as schema_type } from './validator/art'
import { id as schema_guild_id }                          from './validator/guild'
import { assert }                                         from './validator/utils'

import { uuid }                              from 'utils/uuid'
import { NotFoundError, AlreadyExistsError } from 'errors'

const errors = {
  errorIfArtNotExists: (id: string, name: string) => new NotFoundError({
    message: `Erro: A arte com o nome: ${name} não existe no servidor: ${id}.`
  }),
  errorIfArtAlreadyExists: (id: string, name: string) => new AlreadyExistsError({
    message: `Erro: A arte com o nome: ${name} já existe no servidor: ${id}.`
  })
}

type ArtWhereParams = {
  guild_id?: string
  type?:     ArtType
}

type ArtGetherParams = { guild_id: string, id: string }

type ArtCreateParams = { guild_id: string, data: Omit<Partial<Art> & Pick<Art, 'name' | 'type'>, 'guild_id' | 'id'> }

type ArtEditParams = { guild_id: string, id: string, data: Omit<Partial<Art>, 'guild_id' | 'id'> }

type ArtDeleteParams = ArtGetherParams

export default function Arts(db: PrismaClient['art']) {
  async function where({ guild_id, type }: ArtWhereParams): Promise<Art[]> {
    guild_id = !guild_id ? guild_id : assert(schema_guild_id, guild_id)
    type     = !type ? type : assert(schema_type, type)

    const arts = await db.findMany({ where: { guild_id, type }, orderBy: { created_at: 'asc' } })

    return arts;
  }

  async function get({ guild_id, id }: ArtGetherParams): Promise<Art> {
    guild_id = assert(schema_guild_id, guild_id)
    id       = assert(schema_id, id)

    const art = await db.findUnique({ where: { id_guild_id: { guild_id, id } } })

    if(!art) {
      const error = errors['errorIfArtNotExists']

      throw error(guild_id, id);
    }

    return art;
  }

  async function create({ guild_id, data }: ArtCreateParams): Promise<Art> {
    guild_id = assert(schema_guild_id, guild_id)
    
    const { name, type, created_at, updated_at, ...rest } = validate<ArtCreateParams['data']>(data, { required: { name: true, type: true } })

    try {
      const art = await db.create({ data: { name, type, guild_id, id: uuid(), ...rest } })

      return art;
    } catch {
      const error = errors['errorIfArtAlreadyExists']
      
      throw error(guild_id, name);
    }
  }
  async function edit({ guild_id, id, data }: ArtEditParams): Promise<Art> {
    guild_id = assert(schema_guild_id, guild_id)
    id       = assert(schema_id, id)

    const { created_at, updated_at, ...rest } = validate<ArtEditParams['data']>(data, {})

    try {
      const editedArt = await db.update({ where: { id_guild_id: { guild_id, id } }, data: rest })

      return editedArt;
    } catch {
      const error = errors['errorIfArtNotExists']
      
      throw error(guild_id, id);
    }
  }
  async function del({ guild_id, id }: ArtDeleteParams): Promise<Art> {
    guild_id = assert(schema_guild_id, guild_id)
    id       = assert(schema_id, id)

    try {
      const deletedArt = await db.delete({ where: { id_guild_id: { guild_id, id } } })

      return deletedArt as Art;
    } catch {
      const error = errors['errorIfArtNotExists']

      throw error(guild_id, id);
    }
  }

  return { where, get, create, edit, del };
}

export type { Art, ArtType };