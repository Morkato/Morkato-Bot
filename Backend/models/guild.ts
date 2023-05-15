import { NotFoundError, AlreadyExistsError } from 'erros/index'

import valid, { required } from 'models/validator'

import client from 'infra/database'
import Logger from 'infra/logger'


const logger = Logger({
  app: 'models:arts',
  registryLog: true,
  forFormat: '$user $app $func $Server \n\t$type : $message'
})

export interface Guild {
  id: string

  created_at: Date
  updated_at: Date
}

export const getAll = async (): Promise<Guild[]> => {
  return await client.guild.findMany();
}

export async function getGuild(id: string): Promise<Guild> {
  try {
    return await client.guild.findUnique({ where: { id: id } })
  } catch {
    throw new NotFoundError({ message: "Guild ID not found." });
  }
}

export async function getGuilds(rows_id: string[]): Promise<Guild[]> {
  return await client.guild.findMany({
    take: rows_id.length,
    where: { id: { in: rows_id } }
  })
}

export async function createGuild(guild: { id: string }): Promise<Guild> {
  const { id } = valid<{ id: string }>(guild, {
    id: required()
  })

  try {
    return await client.guild.create({ data: { id } })
  } catch {
    throw new AlreadyExistsError({ message: "Guild already exists." })
  }
}

export async function deleteGuild({ id }: Guild): Promise<Guild> {
  try {
    return await client.guild.delete({
      where: {
        id
      }
    })
  } catch {
    throw new NotFoundError({ message: "Guild ID not found." });
  }
}

export default Object.freeze({
  getAll,
  getGuilds,
  getGuild,

  createGuild,

  deleteGuild
})