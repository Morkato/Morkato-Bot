import type { PrismaClient, Prisma } from '@prisma/client'

import valid, { type Variable, assertVariable } from './validator/variables'

import { type Guild, assertGuild } from './validator/guild'

import { assert, schemas } from  './validator/utils'

import {
  NotFoundError,
  AlreadyExistsError
} from 'errors'

export const select: Prisma.VarialbleSelect = {
  name: true,
  text: true,
  visibleCaseIfNotAuthorizerMember: true,

  required_roles: true,
  roles: true,

  created_at: true,
  updated_at: true,

  guild_id: false
}

const errors = {
  errorIfVarNotExists: ({ id }: Guild, name: string) => new NotFoundError({
    message: `Erro: A variável com o nome: ${name} não existe no servidor: ${id}.`
  }),
  errorIfVarAlreadyExists: ({ id }: Guild, name: string) => new AlreadyExistsError({
    message: `Erro: A variável com o nome: ${name} já existe no servidor: ${id}.`
  })
}

export default (db: PrismaClient['varialble']) => {
  async function getAll({ guild }: { guild: Guild }): Promise<Variable[]> {
    assertGuild(guild)

    const vars = await db.findMany({ where: { guild_id: guild.id }, select, orderBy: { created_at: 'asc' } }) as Variable[]

    return vars;
  }
  async function get({ guild, name }: { guild: Guild, name: string }): Promise<Variable> {
    assert(schemas.name.required(), name)
    assertGuild(guild)

    const variable = await db.findUnique({ where: { guild_id_name: { guild_id: guild.id, name } }, select }) as Variable

    if(!variable) {
      const error = errors['errorIfVarNotExists']

      throw error(guild, name);
    }

    return variable;
  }
  async function create({ guild, data }: { guild: Guild, data: any }): Promise<Variable> {
    assertGuild(guild)
    const { name, text, roles, required_roles } = valid(data, {
      required: {
        name: true,
        text: true
      }
    })

    console.log(data)

    try {
      const variable = await db.create({ data: { name, text, required_roles, roles, guild_id: guild.id }, select }) as Variable

      return variable;
    } catch {
      const error = errors['errorIfVarAlreadyExists']

      throw error(guild, data.name);;
    }
  }
  async function edit({ guild, variable, data }: { guild: Guild, variable: Variable, data: any }): Promise<Variable> {
    assertVariable(variable)
    assertGuild(guild)
    data = valid(data, {})

    try {
      const editedArt = await db.update({ where: { guild_id_name: { guild_id: guild.id, name: variable.name } }, data, select }) as Variable

      return editedArt;
    } catch {
      const error = errors['errorIfVarNotExists']

      throw error(guild, variable.name);
    }
  }
  async function del({ guild, variable }: { guild: Guild, variable: Variable }): Promise<Variable>{
    assertVariable(variable)
    assertGuild(guild)

    try {
      const deletedVar = await db.delete({ where: { guild_id_name: { guild_id: guild.id, name: variable.name } }, select }) as Variable

      return deletedVar;
    } catch {
      const error = errors['errorIfVarNotExists']

      throw error(guild, variable.name);
    }
  }

  return { get, getAll, create, edit, del };
}

export type { Variable };