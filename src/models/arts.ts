import type { Art, ArtType, editeArt, Respiration, Kekkijutsu } from 'models/validator/art'

import { Guild } from 'models/validator/guild'

import {
  InternalServerError,
  ValidationError,
  NotFoundError,
  AlreadyExistsError
} from 'errors'

import unidecode from 'remove-accents'
import Logger from 'infra/logger'

import { PrismaClient } from '@prisma/client'

const logger = Logger({
  app: "models:arts",
  forFormat: "$app $func $date $type - $message"
})

const selectMembersInAttacksFields = {
  select: {
    id: true,
    
    text: true,
    roles: true,

    created_at: true,
    updated_at: true
  }
}

const selectMembersInAttacks = {
  select: {
    name: true,

    roles: true,
    required_roles: true,
    required_exp: true,

    damage: true,
    stamina: true,


    embed_title: true,
    embed_description: true,
    embed_url: true,

    fields: selectMembersInAttacksFields,

    created_at: true,
    updated_at: true
  }
}

const selectMembersInArt = {
  name: true,
  type: true,
  role: true,

  embed_title: true,
  embed_description: true,
  embed_url: true,

  attacks: selectMembersInAttacks,
  
  created_at: true,
  updated_at: true
}

const messages = {
  successOnGetAllArts: ({ guild: { id } }: { guild: Guild }) => `Sucesso: Ao obter todos as artes da guilda ID ${id}`,

  errorDataBase: () => `Erro: Infelizmente, nossos serviços não então disponíveis no momento. Pois o banco de dados está offiline.`,
  errorInValidGuild: () => `Erro: A informação do servidor fornecido está incorreta`,
  errorInValidArt: () => `Erro: A informação do servidor fornecido está incorreta`,
  errorIfArtNotExists: ({ id }: Guild, art_name: string) => `Erro: A arte com o nome: ${art_name} não existe no servidor: ${id}.`,
  errorArtAlreadyExists: ({ id }: Guild, art_name: string) => `Erro: A arte com o nome: ${art_name} já existe no servidor: ${id}.`
}

const errors = {
  errorDataBase: () => new InternalServerError({
    message: messages.errorDataBase(),
    statusCode: 500
  }),
  errorInValidGuild: () => new ValidationError({
    message: messages.errorInValidGuild()
  }),
  errorInValidArt: () => new ValidationError({
    message: messages.errorInValidArt()
  }),
  errorIfArtNotExists: (guild: Guild, art_name: string) => new NotFoundError({
    message: messages.errorIfArtNotExists(guild, art_name)
  }),
  errorIfArtAlreadyExists: (guild: Guild, art_name: string) => new AlreadyExistsError({
    message: messages.errorArtAlreadyExists(guild, art_name)
  })
}

export function toKey(text: string) {
  return unidecode(text).trim().toLowerCase();
}

export default function Arts(prisma: PrismaClient['art']) {
  async function getArts(guild: Guild): Promise<Art<ArtType>[]> {
    try {
      const arts = await prisma.findMany({ where: { guild }, select: selectMembersInArt }) as Array<Art<ArtType>>
  
      const message = messages['successOnGetAllArts']
      logger.info(message({ guild }))
  
      return arts;
    } catch {
      const message = messages['errorDataBase']
      logger.error(message(), {})
  
      const error = errors['errorInValidGuild']
      throw error();
    }
  }
  async function getArt({ guild, name }: { guild: Guild, name: string }): Promise<Art<ArtType>> {
    try {
      const art = await prisma.findUnique({ where: { key_guild_id: { key: toKey(name), guild_id: guild.id } }, select: selectMembersInArt }) as Art<ArtType>
  
      if(art) {
        return art;
      }
  
      const message = messages['errorIfArtNotExists']
      logger.warn(message(guild, name))
  
      const error = errors['errorIfArtNotExists']
      throw error(guild, name);
    } catch {
      const message = messages['errorDataBase']
      logger.info(message())
  
      const error = errors['errorDataBase']
      throw error();
    }
  }

  return { getArts, getArt };
}

export type { Art, ArtType, editeArt, Respiration, Kekkijutsu };
