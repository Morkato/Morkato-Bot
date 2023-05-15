import {
  NotFoundError,
  AlreadyExistsError,
  InternalServerError
} from 'errors'

import Logger, { LogSettings } from 'infra/logger'
import valid, { required } from 'models/validator'

import client from 'infra/database'

const logger = Logger({
  app: 'models:arts',
  registryLog: true,
  forFormat: '$user $app $func - $type : $message'
})

const logMessages = {
  dataBaseError: () => "Erro: Parece que o Banco de Dados tem um erro não explícito.",

  successGetAllGuildsInDataBase: () => "Sucesso: Ao obter todos os servidoes do discord no Banco de Dados.",
  successGetGuildFromIDInDataBase: (id: string) => `Sucesso: Ao obter um servidor do discord pelo ID: ${id}`,
  successGetGuildsFromIDInDataBase: (rows_ids: string[]) => {
    const formateIDs =  rows_ids.map(id => `+\t${id}`).join('\n')

    return `Sucesso: Ao obter todos os possíveis servidores do discord filtrando pelos IDs:\n${formateIDs}`
  },
  successOnCreateGuildInDataBase: (id: string) => `Sucesso: Ao criar um novo servidor do discord ID: ${id}`,
  successOnDeleteGuildInDataBase: (id: string) => `Sucesso: Ao deletar um servidor do discord com o ID: ${id}`,
  errorGetAllGuildsInDataBase: () => "Erro: Ao obter todos os servidores do discord no Baco de Dados.",
  errorIfGuildNotExistsInDataBase: (id: string) => `Erro: Ao tentar obter um servidor pelo ID; ${id}.`,
  errorGuildAlreadyExistsInDataBase: (id: string) => `Erro: Ao tentar criar um novo servidor, pois o servidor com o mesmo ID(${id}) já existe`
}

const errors = {
  dataBaseError: () => new InternalServerError({
    message: `500: ${logMessages.dataBaseError()}`,
    action: "Tente relatar à um desenvolvedor."
  }),
  guildNotExistsError: (id: string) => new NotFoundError({
    message: `404: ${logMessages.errorIfGuildNotExistsInDataBase(id)}`,
    action: "Tente criar o servidor primeiro."
  }),
  guildAlreadyExistsError: (id: string) => new AlreadyExistsError({
    message: `400: ${logMessages.errorGuildAlreadyExistsInDataBase(id)}`
  })
}

export type Guild = {
  id: string

  created_at: Date
  updated_at: Date
}

export const getAll = async (logSettings?: LogSettings): Promise<Guild[]> => {
  const settings = { functionName: 'getAll', ...logSettings }
  
  try {
    const guilds = await client.guild.findMany();

    const logMessage = logMessages['successGetAllGuildsInDataBase']
    logger.info(logMessage(), settings)
  
    return guilds;
  } catch {
    const logMessage = logMessages['errorGetAllGuildsInDataBase']
    logger.error(logMessage(), { settings })

    const error = errors['dataBaseError']
    throw error()
  }
}

export async function getGuild(id: string, logSettings?: LogSettings): Promise<Guild> {
  const settings = { functionName: "getGuild", ...logSettings }
  let guild: Guild;
  
  try {
    guild =await client.guild.findUnique({ where: { id: id } })
  } catch {
    const logMessage = logMessages['dataBaseError']
    logger.error(logMessage(), { settings })
  }
  
  if(!guild) {
    const logMessage = logMessages['errorIfGuildNotExists']
    logger.error(logMessage(id), { settings })
    
    const error = errors['guildNotExistsError']
    throw error(id);
  }
  
  const logMessage = logMessages['successGetGuildFromIDInDataBase']
  logger.info(logMessage(id), settings)

  return guild;
  
}

export async function getGuilds(rows_id: string[], logSettings?: LogSettings): Promise<Guild[]> {
  const settings = { functionName: 'getGuilds', ...logSettings }
  
  try {
    const guilds = await client.guild.findMany({
      take: rows_id.length,
      where: { id: { in: rows_id } }
    })

    const logMessage = logMessages['successGetGuildsFromIDInDataBase']
    logger.info(logMessage(rows_id), settings)

    return guilds;
  } catch {
    const logMessage = logMessages['dataBaseError']
    logger.error(logMessage(), { settings })

    const error = errors['dataBaseError']
    throw error()
  }

}

export async function createGuild(guild: { id: string }, logSettings?: LogSettings): Promise<Guild> {
  const settings = { functionName: 'createGuilds', ...logSettings }
  
  const { id } = valid<{ id: string }>(guild, {
    id: required()
  })

  try {
    const guild = await client.guild.create({ data: { id } })

    const logMessage = logMessages['successOnCreateGuildInDataBase']
    logger.info(logMessage(id), settings)

    return guild;
  } catch {
    const logMessage = logMessages['errorGuildAlreadyExistsInDataBase']
    logger.error(logMessage(id), { settings })

    const error = errors['guildAlreadyExistsError']
    throw error(id);
  }
}

export async function deleteGuild({ id }: Guild, logSettings?: LogSettings): Promise<Guild> {
  const settings = { functionName: 'getGuild', ...logSettings }
  
  try {
    const guild = await client.guild.delete({
      where: {
        id
      }
    })

    const logMessage = logMessages['successOnDeleteGuildInDataBase']
    logger.info(logMessage(id), settings)

    return guild;
  } catch {
    const logMessage = logMessages['errorIfGuildNotExistsInDataBase']
    logger.error(logMessage(id), { settings })

    const error = errors['guildNotExistsError']
    throw error(id);
  }
}

export default Object.freeze({
  getAll,
  getGuilds,
  getGuild,

  createGuild,

  deleteGuild
})