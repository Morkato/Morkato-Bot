import type { Player, PlayerBreed } from './validator/player'
import type { PrismaClient }        from '@prisma/client'

import { guild_id as schema_guild_id, id as schema_id, validate } from './validator/player'
import { assert }                                                 from './validator/utils'

import { NotFoundError, AlreadyExistsError } from 'errors'

type PlayerWhere = { guild_id?: string }
type PlayerGether = { guild_id: string, id: string }
type PlayerCreate = PlayerGether & { data: Omit<Partial<Player> & Pick<Player, 'name' | 'breed'>, 'guild_id' | 'id'> }
type PlayerEdit = PlayerGether & { data: Partial<Player> }
type PlayerDelete = PlayerGether

const errors = {
  errorIfPlayerNotExists: (id: string, name: string) => new NotFoundError({
    message: `Erro: O player com o ID: ${name} não existe no servidor: ${id}.`
  }),
  errorIfPlayerAlreadyExists: (id: string, name: string) => new AlreadyExistsError({
    message: `Erro: O player com o ID: ${name} já existe no servidor: ${id}.`
  })
}

export default function Players(db: PrismaClient['player']) {
  async function where({ guild_id }: PlayerWhere): Promise<Player[]> {
    if (guild_id) {
      guild_id = assert(schema_guild_id, guild_id)
    }

    const players = await db.findMany({ where: { guild_id } })

    return players;
  }

  async function get({ guild_id, id }: PlayerGether): Promise<Player> {
    guild_id = assert(schema_guild_id, guild_id)
    id       = assert(schema_id, id)

    const player = await db.findUnique({ where: { guild_id_id: { guild_id, id } } })

    if (!player) {
      const error = errors['errorIfPlayerNotExists']

      throw error(guild_id, id)
    }

    return player;
  }

  async function create({ guild_id, id, data }: PlayerCreate): Promise<Player> {
    guild_id = assert(schema_guild_id, guild_id)
    id       = assert(schema_id, id)

    const { name, breed, ...rest } = validate<PlayerCreate['data']>(data, {
      required: {
        name: true,
        breed: true
      }
    })

    try {
      const player = await db.create({ data: { ...rest, guild_id, id, name, breed } })

      return player;
    } catch {
      const error = errors['errorIfPlayerAlreadyExists']

      throw error(guild_id, id);
    }
  }

  async function edit({ guild_id, id, data }: PlayerEdit): Promise<Player> {
    guild_id = assert(schema_guild_id, guild_id)
    id       = assert(schema_id, id)

    const rest = validate<PlayerEdit['data']>(data, {})

    delete rest.guild_id
    delete rest.id

    const player = await db.update({ where: { guild_id_id: { guild_id, id } }, data: rest })

    return player;
  }

  async function del({ guild_id, id }: PlayerDelete): Promise<Player> {
    guild_id = assert(schema_guild_id, guild_id)
    id       = assert(schema_id, id)

    try {
      const player = await db.delete({ where: { guild_id_id: { guild_id, id } } })

      return player;
    } catch {
      const error = errors['errorIfPlayerNotExists']

      throw error(guild_id, id)
    }
  }

  return { where, get, create, edit, del };
}

export { Players };

export type { Player, PlayerBreed };