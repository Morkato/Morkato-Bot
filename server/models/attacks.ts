import type { PrismaClient } from "@prisma/client"

import { NotFoundError, AlreadyExistsError, ValidationError } from 'morkato/errors'

import { assert, schemas } from 'morkato/schemas/utils'
import { validate } from 'morkato/schemas'

import { strip } from 'morkato/utils/string'
import { created_at, uuid } from 'morkato/utils/uuid'

export type Attack = {
  name: string
  id: string

  required_exp: number

  damage: number
  breath: number
  blood: number

  exclude: boolean

  embed_title: string | null
  embed_description: string | null
  embed_url: string | null

  guild_id: string
  item_id: string | null
  art_id: string | null
  parent_id: string | null

  updated_at: number
}

export function checkIsAttackUniqueByName(name: string, attack: Attack) {
  return strip(name, {
    ignore_accents: true,
    ignore_empty: true,
    case_insensitive: true,
    trim: true
  }) === strip(attack.name, {
    ignore_accents: true,
    ignore_empty: true,
    case_insensitive: true,
    trim: true
  })
}

export function assertAttackAlreadyExists(attacks: Attack[], {
  art_id,
  item_id,
  parent_id,
  name,
  guild_id,
  id
}: Pick<Attack, 'name' | 'guild_id'> & Partial<Pick<Attack, 'id' | 'art_id' | 'item_id' | 'parent_id'>>) {
  const hasOtherAttack = !!attacks.find(attack => attack.guild_id === guild_id && attack.id !== id && (
    parent_id
    && attack.parent_id == parent_id
    || item_id
    && attack.item_id == item_id
    || art_id
  ) && checkIsAttackUniqueByName(name, attack))

  if (hasOtherAttack) {
    throw new AlreadyExistsError({
      message: (art_id
        ? `Erro: O ataque com o nome: ${name} e Arte ID: ${art_id} já existe no servidor: ${guild_id}.`
        : (
          item_id
            ? `Erro: O ataque com o nome: ${name} e Item ID: ${item_id} já existe no servidor: ${guild_id}.`
            : `Erro: O ataque com o nome: ${name} e Ataque Parente ID: ${parent_id} já existe no servidor: ${guild_id}.`
        )
      )
    })
  }
}

type AttackWhereParams = { guild_id?: string, parent_id?: string }
type AttackGetherParams = { guild_id: string, id: string }
type AttackCreateParams = { guild_id: string, data: Omit<Partial<Attack> & Pick<Attack, 'name'>, 'id' | 'guild_id'> }
type AttackEditParams = AttackGetherParams & { data: Partial<AttackCreateParams['data']> }
type AttackDeleteParams = AttackGetherParams

interface AttacksMembers {
  where({ guild_id, parent_id }: AttackWhereParams): Promise<Attack[]>
  get({ guild_id, id }: AttackGetherParams): Promise<Attack>
  create({ guild_id, data }: AttackCreateParams): Promise<Attack>
  edit({ guild_id, id, data }: AttackEditParams): Promise<{ before: Attack, after: Attack }>
  del({ guild_id, id }: AttackDeleteParams): Promise<Attack>
}

export default function Attacks(db: PrismaClient['attack']): AttacksMembers {
  async function where({ guild_id, parent_id }: AttackWhereParams): Promise<Attack[]> {
    guild_id = !guild_id ? guild_id : assert(schemas.id, guild_id)
    parent_id = !parent_id ? parent_id : assert(schemas.id, parent_id)

    const attacks = await db.findMany({ where: { guild_id, parent_id }, orderBy: { id: 'asc' } })

    return attacks.map(attack => ({ ...attack, exclude: attack.exclude === 'true', updated_at: Number(attack.updated_at) }));
  }

  async function get({ guild_id, id }: AttackGetherParams): Promise<Attack> {
    guild_id = assert(schemas.id, guild_id)
    id = assert(schemas.id, id)

    const attack = await db.findUnique({ where: { guild_id_id: { guild_id, id } } })

    if (!attack) {
      throw new NotFoundError({
        message: `Erro: O ataque com o ID: ${id} não existe no servidor: ${guild_id}.`
      })
    }

    return { ...attack, exclude: attack.exclude === 'true', updated_at: Number(attack.updated_at) };
  }

  async function create({ guild_id, data }: AttackCreateParams): Promise<Attack> {
    guild_id = assert(schemas.id, guild_id)

    const { name, item_id, art_id, parent_id, ...rest } = validate(data, {
      name: 'required',

      required_exp: 'optional',

      damage: 'optional',
      breath: 'optional',
      blood: 'optional',

      exclude: 'optional',

      embed_title: 'optional',
      embed_description: 'optional',
      embed_url: 'optional',

      item_id: 'optional',
      art_id: 'optional',
      parent_id: 'optional'
    }) as Partial<Omit<Attack, 'id' | 'guild_id' | 'created_at' | 'updated_at'>> & Pick<Attack, 'name'>

    if (!item_id && !art_id && !parent_id) {
      throw new ValidationError({
        message: "arm_id, art_id or parent_id is required!"
      })
    }

    const hasExtends = [item_id, art_id, parent_id].filter(o => !!o).length !== 1

    if (hasExtends) {
      throw new ValidationError({
        message: "arm_id, art_id or parent_id only!"
      })
    }

    const attacks = await where({ guild_id })

    assertAttackAlreadyExists(attacks, { item_id, art_id, parent_id, name, guild_id })

    const id = uuid()
    const updated_at = created_at(id)

    const attack = await db.create({
      data: {
        ...rest,
        guild_id,
        id,
        name,
        item_id,
        art_id,
        parent_id,
        updated_at,

        exclude: rest.exclude === undefined ? undefined : rest.exclude ? 'true' : 'false'
      }
    })

    return { ...attack, exclude: attack.exclude === 'true', updated_at: Number(attack.updated_at) };
  }

  async function edit({ guild_id, id, data }: AttackEditParams): Promise<{ before: Attack, after: Attack }> {
    guild_id = assert(schemas.id, guild_id)
    id = assert(schemas.id, id)

    const { name, ...rest } = validate(data, {
      name: 'optional',

      required_exp: 'optional',

      damage: 'optional',
      breath: 'optional',
      blood: 'optional',

      exclude: 'optional',

      embed_title: 'optional',
      embed_description: 'optional',
      embed_url: 'optional'
    })

    const attacks = await where({ guild_id })

    const before = attacks.find(attack => attack.id === id)

    if (!before) {
      throw new NotFoundError({
        message: `Erro: O ataque com o ID: ${id} não existe no servidor: ${guild_id}.`
      })
    }

    if (name) {
      assertAttackAlreadyExists(attacks, { ...before, name })
    }

    try {
      const after = await db.update({
        where: { guild_id_id: { guild_id, id } },
        data: {
          ...rest,
          name,
          exclude: rest.exclude === undefined ? undefined : rest.exclude ? 'true' : 'false'
        }
      })

      return { before, after: { ...after, exclude: after.exclude === 'true', updated_at: Number(after.updated_at) } };
    } catch {
      throw new NotFoundError({
        message: `Erro: O ataque com o ID: ${id} não existe no servidor: ${guild_id}.`
      })
    }
  }

  async function del({ guild_id, id }: AttackDeleteParams): Promise<Attack> {
    guild_id = assert(schemas.id, guild_id)
    id = assert(schemas.id, id)

    try {
      const attack = await db.delete({
        where: { guild_id_id: { guild_id, id } }
      })

      return { ...attack, exclude: attack.exclude === 'true', updated_at: Number(attack.updated_at) };
    } catch {
      throw new NotFoundError({
        message: `Erro: O ataque com o ID: ${id} não existe no servidor: ${guild_id}.`
      })
    }
  }

  return { where, get, create, edit, del };
}

export { Attacks };
