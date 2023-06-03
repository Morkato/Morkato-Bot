import type { PrismaClient } from '@prisma/client'

import {
  NotFoundError,
  AlreadyExistsError,
  InternalServerError
} from 'errors'

import { assertSchema, schemas } from './validator/utils'

import Logger, { LogSettings } from 'infra/logger'
import valid, { validateGuild, Guild } from './validator/guild'
import Joi from 'joi'

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
    const formateIDs = rows_ids.map(id => `+\t${id}`).join('\n')

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

export default function Guilds(db: PrismaClient['guild']) {
  return Object.assign(db, {
    async getAll(logSettings?: LogSettings): Promise<Guild[]> {
      const settings = { functionName: 'getAll', ...logSettings }

      try {
        const guilds = await db.findMany();

        const logMessage = logMessages['successGetAllGuildsInDataBase']
        logger.info(logMessage(), settings)

        return guilds;
      } catch {
        const logMessage = logMessages['errorGetAllGuildsInDataBase']
        logger.error(logMessage(), { settings })

        const error = errors['dataBaseError']
        throw error()
      }
    },
    async getGuild(id: string, logSettings?: LogSettings): Promise<Guild> {
      const settings = { functionName: "getGuild", ...logSettings }
      let guild: Guild;

      assertSchema(schemas.id.required(), id)
    
      try {
        guild = await db.findUnique({ where: { id: id } })
      } catch (err) {
        const logMessage = logMessages['dataBaseError']
        logger.error(logMessage(), { settings })
    
        const error = errors['dataBaseError']
        throw error();
      }
    
      if (!guild) {
        const logMessage = logMessages['errorIfGuildNotExistsInDataBase']
        logger.error(logMessage(id), { settings })
    
        const error = errors['guildNotExistsError']
        throw error(id);
      }
    
      const logMessage = logMessages['successGetGuildFromIDInDataBase']
      logger.info(logMessage(id), settings)
    
      return guild;
    },
    async getGuilds(rows_id: string[], logSettings?: LogSettings): Promise<Guild[]> {
      const settings = { functionName: 'getGuilds', ...logSettings }

      assertSchema(schemas.arrayId.required(), rows_id)
    
      try {
        const guilds = await db.findMany({
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
    },
    async createGuild({ id }: { id: string }, logSettings?: LogSettings): Promise<Guild> {
      const settings = { functionName: 'createGuilds', ...logSettings }

      assertSchema(schemas.id.required(), id)
    
      try {
        const guild = await db.create({ data: { id } })
    
        const logMessage = logMessages['successOnCreateGuildInDataBase']
        logger.info(logMessage(id), settings)
    
        return guild;
      } catch {
        const logMessage = logMessages['errorGuildAlreadyExistsInDataBase']
        logger.error(logMessage(id), { settings })
    
        const error = errors['guildAlreadyExistsError']
        throw error(id);
      }
    },
    async deleteGuild(guild: Guild, logSettings?: LogSettings): Promise<Guild> {
      const settings = { functionName: 'getGuild', ...logSettings }

      validateGuild(guild)
    
      const { id } = guild
    
      try {
        const guild = await db.delete({
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
  })
}

export type { Guild };

export { Guilds };