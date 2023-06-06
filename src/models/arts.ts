import valid, { 
  Art,
  ArtType,
  editeArt,
  Respiration,
  Kekkijutsu,

  validateArt
} from 'models/validator/art'

import {
  selectMembersInAttacks
} from 'models/attacks'

import { Guild, validateGuild } from 'models/validator/guild'

import { assertSchema, schemas } from './validator/utils'

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

export const selectMembersInArt = {
  name: true,
  type: true,
  role: true,

  embed_title: true,
  embed_description: true,
  embed_url: true,

  attacks: { select: selectMembersInAttacks, orderBy: { created_at: 'asc' } },
  
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
  return unidecode(text).trim().toLowerCase().replace(' ', '-');
}

export default function Arts(prisma: PrismaClient['art']) {
  async function getArts(guild: Guild): Promise<Art<ArtType>[]> {
    validateGuild(guild)

    try {
      const arts = await prisma.findMany({ where: { guild }, select: selectMembersInArt, orderBy: { created_at: 'asc' } }) as Array<Art<ArtType>>
  
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
    name = assertSchema(schemas.name.required(), name)
    validateGuild(guild)
    
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
  async function createArt({ guild, data }: { guild: Guild, data: Partial<Art<ArtType>> }): Promise<Art<ArtType>> {
    data = valid(data, {
      required: {
        name: true,
        type: true
      }
    })
    validateGuild(guild)

    try {
      const art = await prisma.create({ data: { name: data.name, key: toKey(data.name), type: data.type, guild_id: guild.id }, select: selectMembersInArt })

      return art;
    } catch {
      const message = messages['errorArtAlreadyExists']
      logger.info(message(guild, data.name))

      const error = errors['errorIfArtAlreadyExists']
      throw error(guild, data.name);
    }
  }
  async function editArt({ guild, art, data }: { guild: Guild, art: Art<ArtType>, data: Omit<Partial<Art<ArtType>>, 'attacks'> }): Promise<Art<ArtType>> {
    validateGuild(guild)
    validateArt(art)

    try {
      const editedArt = await prisma.update({ where: { key_guild_id: { key: toKey(art.name), guild_id: guild.id } }, data: data, select: selectMembersInArt })

      return editedArt;
    } catch {
      const message = messages['errorIfArtNotExists']
      logger.warn(message(guild, art.name))

      const error = errors['errorIfArtNotExists']
      throw error(guild, art.name);
    }
  }
  async function delArt({ guild, art }: { guild: Guild, art: Art<ArtType> }): Promise<Art<ArtType>> {
    validateGuild(guild)
    validateArt(art)

    try {
      const deletedArt = await prisma.delete({ where: { key_guild_id: { key: toKey(art.name), guild_id: guild.id } }, select: selectMembersInArt })

      return deletedArt;
    } catch {
      const message = messages['errorIfArtNotExists']
      logger.warn(message(guild, art.name))

      const error = errors['errorIfArtNotExists']
      throw error(guild, art.name);
    }
  }

  return { getArts, getArt, createArt, editArt, delArt };
}

export type { Art, ArtType, editeArt, Respiration, Kekkijutsu };
