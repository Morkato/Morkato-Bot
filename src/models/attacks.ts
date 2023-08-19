import type { Attack }       from './validator/attack'
import type { PrismaClient } from "@prisma/client"

import { validate, guild_id as schema_guild_id, art_id as schema_art_id, id as schema_id, parent_id as schema_parent_id } from "./validator/attack"
import { assert }                                                                                                         from "./validator/utils"

import { uuid }                              from 'utils/uuid'
import { NotFoundError, AlreadyExistsError } from 'errors'

const errors = {
  errorIfAttackNotExists: (id: string, name: string) => new NotFoundError({
    message: `Erro: O ataque com o nome: ${name} não existe no servidor: ${id}.`
  }),
  errorIfAttackAlreadyExists: (id: string, name: string) => new AlreadyExistsError({
    message: `Erro: O ataque com o nome: ${name} já existe no servidor: ${id}.`
  })
}

type AttackWhereParams = { guild_id?: string, art_id?: string, parent_id?: string }

type AttackGetherParams = { guild_id: string, id: string }

type AttackCreateParams = { guild_id, data: Omit<Partial<Attack> & Pick<Attack, 'name'>, 'id' | 'guild_id'> }

type AttackEditParams = AttackGetherParams & { data: Partial<AttackCreateParams['data']> }

type AttackDeleteParams = AttackGetherParams

export default function Attacks(db: PrismaClient['attack']) {
  async function where({ guild_id, art_id, parent_id }: AttackWhereParams): Promise<Attack[]> {
    guild_id  = !guild_id ? guild_id : assert(schema_guild_id, guild_id)
    art_id    = !art_id ? art_id : assert(schema_art_id, art_id)
    parent_id = !parent_id ? parent_id : assert(schema_parent_id, parent_id)

    const attacks = await db.findMany({ where: { guild_id, art_id, parent_id }, orderBy: { created_at: 'asc' } })

    return attacks as Attack[];
  }

  async function get({ guild_id, id }: AttackGetherParams): Promise<Attack> {
    guild_id = assert(schema_guild_id, guild_id)
    id       = assert(schema_id, id)

    const attack = await db.findUnique({ where: { id_guild_id: { guild_id, id } } })

    if(!attack) {
      const error = errors['errorIfAttackNotExists']

      throw error(guild_id, id);
    }

    return attack as Attack;
  }

  async function create({ guild_id, data }: AttackCreateParams) {
    guild_id = assert(schema_guild_id, guild_id)

    const { name, created_at, updated_at, ...rest } = validate<AttackCreateParams['data']>(data, { required: { name: true } })

    try {
      const attack = await db.create({ data: { name, guild_id, id: uuid(), ...rest } })

      return attack as Attack;
    } catch {
      const error = errors['errorIfAttackAlreadyExists']

      throw error(guild_id, name);
    }
  }

  async function edit({ guild_id, id, data }: AttackEditParams): Promise<Attack> {
    guild_id = assert(schema_guild_id, guild_id)
    id       = assert(schema_id, id)

    const { art_id, created_at, updated_at, ...rest } = validate<AttackEditParams['data']>(data, {})

    try {
      const editedAttack = await db.update({ where: { id_guild_id: { guild_id, id } }, data: rest })

      return editedAttack as Attack;
    } catch {
      const error = errors['errorIfAttackNotExists']

      throw error(guild_id, id);
    }
  }

  async function del({ guild_id, id }: AttackGetherParams): Promise<Attack> {
    guild_id = assert(schema_guild_id, guild_id)
    id       = assert(schema_id, id)

    try {
      const deletedAttack = await db.delete({ where: { id_guild_id: { guild_id, id } } })

      return deletedAttack as Attack;
    } catch {
      const error = errors['errorIfAttackNotExists']

      throw error(guild_id, id);
    }
  }

  return { where, get, create, edit, del };
}

export { Attacks, type Attack };