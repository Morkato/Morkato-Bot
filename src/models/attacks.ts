import type { PrismaClient, Prisma } from "@prisma/client"

import { type Guild,  assertGuild }  from 'models/validator/guild'
import { type Art,    assertArt }    from 'models/validator/art'
import { type Attack, assertAttack } from "./validator/attack"

import { assert, schemas } from "./validator/utils"

import { toKey } from 'utils'

import {
  NotFoundError,
  AlreadyExistsError
} from 'errors'

export const select: Prisma.AttackSelect = {
  name: true,

  roles: true,
  required_roles: true,
  required_exp: true,

  damage: true,
  stamina: true,

  embed_title: true,
  embed_description: true,
  embed_url: true,

  created_at: true,
  updated_at: true
}

const errors = {
  errorIfAttackNotExists: ({ id }: Guild, name: string) => new NotFoundError({
    message: `Erro: O ataque com o nome: ${name} não existe no servidor: ${id}.`
  }),
  errorIfAttackAlreadyExists: ({ id }: Guild, name: string) => new AlreadyExistsError({
    message: `Erro: O ataque com o nome: ${name} já existe no servidor: ${id}.`
  })
}

export default function Attacks(prisma: PrismaClient['attack']) {
  async function getAll({ guild, art }: { guild: Guild, art: Art }): Promise<Attack[]> {
    assertGuild(guild)
    assertArt(art)

    const attacks = await prisma.findMany({ where: { guild_id: guild.id, art_key: toKey(art.name) }, select, orderBy: { created_at: 'asc' }  })

    return attacks as Attack[];
  }
  async function get({ guild, name }: { guild: Guild, name: string }): Promise<Attack> {
    name = assert(schemas.name.required(), name)
    assertGuild(guild)

    const attack = await prisma.findUnique({ where: { key_guild_id: { key: toKey(name), guild_id: guild.id } }, select })

    if(!attack) {
      const error = errors['errorIfAttackNotExists']

      throw error(guild, name);
    }

    return attack as Attack;
  }
  async function create({ guild, art, name }: { guild: Guild, art: Art, name: string }) {
    name = assert(schemas.name.required(), name)
    assertGuild(guild)
    assertArt(art)

    try {
      const attack = await prisma.create({ data: { art_key: toKey(art.name), guild_id: guild.id, name, key: toKey(name) }, select })

      art.attacks.push(attack as Attack)

      return attack as Attack;
    } catch {
      const error = errors['errorIfAttackAlreadyExists']

      throw error(guild, name);
    }
  }
  async function edit({ guild, attack, data }: { guild: Guild, attack: Attack, data: Omit<Partial<Attack>, 'fields'> }): Promise<Attack> {
    assertAttack(attack)
    assertGuild(guild)

    try {
      const editedAttack = await prisma.update({ where: { key_guild_id: { key: toKey(attack.name), guild_id: guild.id } }, data, select })

      return editedAttack as Attack;
    } catch {
      const error = errors['errorIfAttackNotExists']

      throw error(guild, attack.name);
    }
  }
  async function del({ guild, attack }: { guild: Guild, attack: Attack }): Promise<Attack> {
    assertAttack(attack)
    assertGuild(guild)

    try {
      const deletedAttack = await prisma.delete({ where: { key_guild_id: { key: toKey(attack.name), guild_id: guild.id } }, select })

      return deletedAttack as Attack;
    } catch {
      const error = errors['errorIfAttackNotExists']

      throw error(guild, attack.name);
    }
  }

  return { getAll, get, create, edit, del };
}

export { Attacks, type Attack };