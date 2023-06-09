import valid, { 
  type Art,
  type ArtType,
  type editeArt,

  assertArt
} from './validator/art'

import {
  select as selectMembersInAttacks
} from 'models/attacks'

import { Guild, assertGuild } from 'models/validator/guild'

import { assert, schemas } from './validator/utils'

import { toKey } from 'utils'

import {
  NotFoundError,
  AlreadyExistsError
} from 'errors'

import { PrismaClient, Prisma } from '@prisma/client'

export const select: Prisma.ArtSelect = {
  name: true,
  type: true,
  role: true,

  embed_title: true,
  embed_description: true,
  embed_url: true,

  attacks: { select: selectMembersInAttacks, orderBy: { created_at: 'asc' } },
  
  created_at: true,
  updated_at: true
}

const errors = {
  errorIfArtNotExists: ({ id }: Guild, name: string) => new NotFoundError({
    message: `Erro: A arte com o nome: ${name} não existe no servidor: ${id}.`
  }),
  errorIfArtAlreadyExists: ({ id }: Guild, name: string) => new AlreadyExistsError({
    message: `Erro: A arte com o nome: ${name} já existe no servidor: ${id}.`
  })
}

export default function Arts(db: PrismaClient['art']) {
  async function getAll(guild: Guild): Promise<Art[]> {
    assertGuild(guild)
    
    const arts = await db.findMany({ where: { guild_id: guild.id }, select, orderBy: { created_at: 'asc' } })

    return arts as Art[];
  }
  async function get({ guild, name }: { guild: Guild, name: string }): Promise<Art> {
    name = assert(schemas.name.required(), name)
    assertGuild(guild)

    const art = await db.findUnique({ where: { key_guild_id: { key: toKey(name), guild_id: guild.id } }, select })

    if(!art) {
      const error = errors['errorIfArtNotExists']

      throw error(guild, name);
    }

    return art as Art;
  }
  async function create({ guild, data }: { guild: Guild, data: Partial<Omit<Art, 'attacks'>> }): Promise<Art> {
    const {
      name,
      type,
      role,

      embed_title,
      embed_description,
      embed_url
    } = valid(data, {
      required: {
        name: true,
        type: true
      }
    })
    assertGuild(guild)

    try {
      const art = await db.create({ data: {
        name,
        type,
        role,

        embed_title,
        embed_description,
        embed_url,

        key: toKey(name),
        guild_id: guild.id
      }, select })

      return art as Art;
    } catch {
      const error = errors['errorIfArtAlreadyExists']
      
      throw error(guild, data.name);
    }
  }
  async function editArt({ guild, art, data }: { guild: Guild, art: Art, data: Omit<Partial<Art>, 'attacks'> }): Promise<Art> {
    assertGuild(guild)
    assertArt(art)

    let {
      name,
      type,
      role,
      key,

      embed_title,
      embed_description,
      embed_url
    } = valid(data, {})

    if(name) {
      key = toKey(name)
    }

    try {
      const editedArt = await db.update({ where: { key_guild_id: { key: toKey(art.name), guild_id: guild.id } }, data: {
        name,
        type,
        role,
        key,

        embed_title,
        embed_description,
        embed_url
      }, select })

      return editedArt as Art;
    } catch {
      const error = errors['errorIfArtNotExists']
      
      throw error(guild, art.name);
    }
  }
  async function delArt({ guild, art }: { guild: Guild, art: Art }): Promise<Art> {
    assertGuild(guild)
    assertArt(art)

    try {
      const deletedArt = await db.delete({ where: { key_guild_id: { key: toKey(art.name), guild_id: guild.id } }, select })

      return deletedArt as Art;
    } catch {
      const error = errors['errorIfArtNotExists']

      throw error(guild, art.name);
    }
  }

  return { getAll, get, create, editArt, delArt };
}

export type { Art, ArtType, editeArt };