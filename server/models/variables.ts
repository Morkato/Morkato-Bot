import type { PrismaClient, Prisma } from '@prisma/client'

import valid, { type Variable } from './validator/variables'
import { assert, schemas }      from './validator/utils'

import {
  NotFoundError,
  AlreadyExistsError
} from 'errors'

export const select: Prisma.VariableSelect = {
  name: true,
  text: true,

  required_roles: true,
  roles: true,

  created_at: true,
  updated_at: true,

  guild_id: true
}

const errors = {
  errorIfVarNotExists: (guild_id: string, name: string) => new NotFoundError({
    message: `Erro: A variável com o nome: ${name} não existe no servidor: ${guild_id}.`
  }),
  errorIfVarAlreadyExists: (guild_id: string, name: string) => new AlreadyExistsError({
    message: `Erro: A variável com o nome: ${name} já existe no servidor: ${guild_id}.`
  })
}

export default (db: PrismaClient['variable']) => {
  async function getAll({ guild_id }: { guild_id: string }): Promise<Variable[]> {
    assert(schemas.id.required(), guild_id)

    const vars = await db.findMany({ where: { guild_id }, select, orderBy: { created_at: 'asc' } }) as Variable[]

    return vars;
  }
  async function get({ guild_id, name }: { guild_id: string, name: string }): Promise<Variable> {
    assert(schemas.id.required(), guild_id)
    assert(schemas.name.required(), name)  

    const variable = await db.findUnique({ where: { guild_id_name: { guild_id, name } }, select }) as Variable

    if(!variable) {
      const error = errors['errorIfVarNotExists']

      throw error(guild_id, name);
    }

    return variable;
  }
  async function create({ guild_id, data }: { guild_id: string, data: any }): Promise<Variable> {
    assert(schemas.id.required(), guild_id)

    const { name, text, roles, required_roles } = valid(data, {
      required: {
        name: true,
        text: true
      }
    })    

    try {
      const variable = await db.create({ data: { name, text, required_roles, roles, guild_id }, select }) as Variable

      return variable;
    } catch {
      const error = errors['errorIfVarAlreadyExists']

      throw error(guild_id, data.name);
    }
  }
  async function edit({ guild_id, name, data }: { guild_id: string, name: string, data: any }): Promise<Variable> {
    assert(schemas.id.required(), guild_id)
    assert(schemas.name.required(), name)
    
    data = valid(data, {})

    try {
      const editedArt = await db.update({ where: { guild_id_name: { guild_id, name } }, data, select }) as Variable

      return editedArt;
    } catch {
      const error = errors['errorIfVarNotExists']

      throw error(guild_id, name);
    }
  }
  async function del({ guild_id, name }: { guild_id: string, name: string}): Promise<Variable>{
    assert(schemas.id.required(), guild_id)
    assert(schemas.name.required(), name)

    try {
      const deletedVar = await db.delete({ where: { guild_id_name: { guild_id, name } }, select }) as Variable

      return deletedVar;
    } catch {
      const error = errors['errorIfVarNotExists']

      throw error(guild_id, name);
    }
  }

  return { get, getAll, create, edit, del };
}

export type { Variable };