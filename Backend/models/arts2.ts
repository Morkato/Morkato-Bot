import { Guild, isValidGuild } from 'models/guild'

import {
  InternalServerError,
  ValidationError,
  NotFoundError,
  AlreadyExistsError
} from 'errors'

import Logger, { LogSettings } from 'infra/logger'
import valid from 'models/validator (deprecated-2)'

import { PrismaClient } from '@prisma/client'
import unidecode from 'remove-accents'
import client from 'infra/database'

const logger = Logger({
  app: "models:arts",
  forFormat: "$app $func $date $type - $message"
})

type AttackField = {
  id: string

  text: string
  roles: string[]

  created_at: Date
  updated_at: Date
}

type Attack = {
  name: string

  roles: string[]
  required_roles: number
  required_exp: number

  damage: number
  stamina: number

  embed_title: string | null
  embed_description: string | null
  embed_url: string | null

  fields: AttackField[]

  created_at: Date
  updated_at: Date
}

type ArtType = "RESPIRATION" | "KEKKIJUTSU" | "ATTACK"
type Art<Type extends ArtType> = {
  name: string
  type: Type
  role: string | null

  embed_title: string | null
  embed_description: string | null
  embed_url: string | null

  attacks: Attack[]

  created_at: Date
  updated_at: Date
}

type editeArt<Type extends ArtType> = Partial<Omit<Art<Type>, 'attacks' | 'created_at' | 'updated_at'>>

interface Respiration extends Art<"RESPIRATION"> {  }
interface Kekkijutsu extends Art<"KEKKIJUTSU"> {  }

interface editeRespiration extends editeArt<"RESPIRATION"> {  }
interface editeKekkijutsu extends editeArt<"KEKKIJUTSU"> {  }

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
  successOnGetAllArts: ({ guild: { id }, type }: { guild: Guild, type: ArtType }) => `Sucesso: Ao obter todos as artes com o tipo: ${type} da guilda ID ${id}`,

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

export function isValidArt(art: Art<ArtType>) {
  try {
    const validateArt = valid(art, {
      name: 'required',
      type: 'required',
      role: 'required',

      embed_title: 'required',
      embed_description: 'required',
      embed_url: 'required',

      created_at: 'required',
      updated_at: 'required'
    }, { params: {
      type: [['ATTACK', 'RESPIRATION', 'KEKKIJUTSU']]
    } })

    return !!validateArt;
  } catch {
    return false;
  }
}

export async function getArts<Type extends ArtType>({ guild, type }: { guild: Guild, type: Type }) {
  if(!isValidGuild(guild)) {
    const message = messages['errorInValidGuild']
    logger.error(message(), {})
    
    const error = errors['errorInValidGuild']
    throw error()
  }

  try {
    const arts = await client.art.findMany({ where: { guild, type }, select: selectMembersInArt }) as Array<Art<ArtType>>

    const message = messages['successOnGetAllArts']
    logger.info(message({ guild, type }))

    return arts as Array<Art<Type>>;
  } catch {
    const message = messages['errorDataBase']
    logger.error(message(), {})

    const error = errors['errorInValidGuild']
    throw error();
  }
}

export async function getArt<Type extends ArtType>({ guild, type, name }: { guild: Guild, type: Type, name: string }): Promise<Art<Type>> {
  if(!isValidGuild(guild)) {
    const message = messages['errorInValidGuild']
    logger.error(message(), {})
    
    const error = errors['errorInValidGuild']
    throw error()
  }
  
  try {
    const art = await client.art.findFirst({ where: { name: { contains: name, mode: 'insensitive',  }, guild, type }, select: selectMembersInArt }) as Art<ArtType>

    if(art) {
      return art as Art<Type>;
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

export async function createArt<Type extends ArtType>({ guild, art }: { guild: Guild, art: editeArt<Type>}) {
  if(!isValidGuild(guild)) {
    const message = messages['errorInValidGuild']
    logger.error(message(), {})
    
    const error = errors['errorInValidGuild']
    throw error()
  }

  const {
    name,
    type,
    role,

    embed_title,
    embed_description,
    embed_url
  } = valid(art, {
    name: 'required',
    type: 'required',
    role: 'optional',

    embed_title: 'optional',
    embed_description: 'optional',
    embed_url: 'optional'
  }, {
    params: {
      type: [['ATTACK', 'RESPIRATION', 'KEKKIJUTSU']],
      role: [null],
      embed_title: [null],
      embed_description: [null],
      embed_url: [null]
    }
  }) as editeArt<Type>

  if(await getArt({ guild, name, type })) {
    const message = messages['errorArtAlreadyExists']
    logger.info(message(guild, art.name))

    const error = errors['errorIfArtAlreadyExists']
    throw error(guild, art.name);
  }

  try {
    const newArt = await client.art.create({ data: {
      name,
      type,
      role,

      guild_id: guild.id,
      embed_title,
      embed_description,
      embed_url
    }, select: selectMembersInArt }) as Art<ArtType>

    return newArt as Art<Type>;
  } catch {
    const message = messages['errorDataBase']
    logger.info(message())

    const error = errors['errorDataBase']
    throw error();
  }
}

export async function editArt<Type extends ArtType>({ guild, art, to }: { guild: Guild, art: Art<Type>, to: editeArt<Type> }) {
  if(!isValidGuild(guild)) {
    const message = messages['errorInValidGuild']
    logger.error(message(), {})
    
    const error = errors['errorInValidGuild']
    throw error()
  }

  try {
    if(!isValidArt(art)) {
      const message = messages['errorInValidArt']
      logger.error(message(), {})
      
      const error = errors['errorInValidArt']
      throw error()
    }
    
    const data = valid(to, {
      name: 'optional',
      type: 'optional',
      role: 'optional',

      embed_title: 'optional',
      embed_description: 'optional',
      embed_url: 'optional'
    }, {
      params: {
        name: [art.name],
        type: [['ATTACK', 'RESPIRATION', 'KEKKIJUTSU'], art.type],
        role: [art.role],

        embed_title: [art.embed_title],
        embed_description: [art.embed_description],
        embed_url: [art.embed_url]
      }
    }) as editeArt<Type>

    const editedArt = await client.art.update({
      data,
      where: {
        name_guild_id: { name: art.name, guild_id: guild.id }
      },
      select: selectMembersInArt
    }) as Art<ArtType>

    return editedArt as Art<Type>;
  } catch {
    const message = messages['errorDataBase']
    logger.info(message())

    const error = errors['errorDataBase']
    throw error();
  }
}

export default function Arts(prismaArts: PrismaClient['art']) {
  return Object.assign(prismaArts, getArts, {
    getArt,
    createArt
  })
}

