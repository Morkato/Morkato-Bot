import valid, { required, optional } from 'models/validator'
import Logger, { LogSettings } from 'infra/logger'

import {
  NotFoundError,
  AlreadyExistsError,
  InternalServerError
} from 'errors/index'

import client from 'infra/database'

const logger = Logger({
  app: 'models:arts',
  registryLog: true,
  forFormat: '$user $app $func $type : $message'
})

type AttackFields = {
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

  damage: number
  stamina: number

  embed_title: string | null
  embed_description: string | null
  embed_url: string | null

  fields: AttackFields[]

  created_at: Date
  updated_at: Date
}

type ArtType = "ATTACK" | "RESPIRATION" | "KEKKIJUTSU"

export type OriginalArt = {
  name: string
  type: ArtType
  role: string | null
  
  guild_id: string

  embed_title: string | null
  embed_description: string | null
  embed_url: string | null
}

export type Art = {
  name: string
  type: ArtType
  role: string | null
  

  embed_title: string | null
  embed_description: string | null
  embed_url: string | null

  created_at: Date
  updated_at: Date

  attacks: Attack[]
}

export interface Respiration extends Art {  }
export interface Kekkijutsu extends Art {  }

const logMessages = {
  dataBaseError: () => "Erro: Parece que o Banco de Dados tem um erro não explícito.",

  successOnGetAll: () => `Sucesso: Ao obter todas as artes do Banco de Dados.`,
  successOnGetAllFromGuild: (id: string) => `Sucesso: Ao obter todas as artes do servidor ID: ${id}.`,
  successOnGetAllFromType: (type: ArtType) => `Sucesso: Ao obter todas as artes do Banco de Dados filtrando pelo tipo: ${type}.`,
  successOnGetAllFromGuildAndType: (id: string, type: ArtType) => `Sucesso: Ao obter todas as artes do servidor ID: ${id} filtrando pelo tipo: ${type}.`,
  successOnGetArtFromGuildTypeAndName: (guild_id: string, { name, type }: Art) => `Sucesso: Ao obter a arte nome: ${name} e tipo: ${type} do servidor ID: ${guild_id}.`,
  
  successOnCreateArt: (guild_id: string, { name, type }: Art) => `Sucesso: Ao criar uma nova arte com o nome: ${name} e tipo: ${type} no servidor ID: ${guild_id}.`,
  successOnEditArt: (guild_id: string, { name, type }: Art) => `Sucesso: Ao editar a arte com o nome: ${name} e tipo: ${type} no servidor ID: ${guild_id}.`,
  successOnDeleteArt: (guild_id: string, { name, type }: Art) => `Sucesso: Ao deletar a arte com o nome: ${name} e tipo: ${type} no servidor ID: ${guild_id}.`,

  errorOnGetArtFromType: (guild_id: string, { name, type }: { name: string, type: ArtType }) => `Erro: Ao obter a arte nome: ${name} e tipo: ${type} do servidor ID: ${guild_id}.`,
  
  errorOnCreateArt: (guild_id: string, { name, type }: { name: string, type: ArtType }) => `Erro: Ao criar uma nova arte com o nome: ${name} e tipo: ${type} no servidor ID: ${guild_id}, pois já existe uma arte com essas características.`
}

const errors = {
  dataBaseError: () => new InternalServerError({
    message: `500: ${logMessages.dataBaseError()}`,
    action: "Tente relatar à um desenvolvedor."
  }),
  artNotExists: (guild_id: string, { name, type }: { name: string, type: ArtType }) => new NotFoundError({
    message: `404: ${logMessages.errorOnGetArtFromType(guild_id, { name, type })}`,
    action: "Tente criar a arte primeiro."
  }),
  artAlreadyExists: (guild_id: string, { name, type }: { name: string, type: ArtType }) => new AlreadyExistsError({
    message: `400: ${logMessages.errorOnCreateArt(guild_id, { name, type })}`
  })
}

const attackFieldsSelect = {
  id: true,

  text: true,
  roles: true,

  created_at: true,
  updated_at: true,

  attack_name: false,
  guild_id: false
}

const attackSelect = {
  name: true,

  roles: true,
  required_roles: true,

  damage: true,
  stamina: true,

  embed_title: true,
  embed_description: true,
  embed_url: true,

  created_at: true,
  updated_at: true,

  fields: {
    select: attackFieldsSelect
  },

  guild_id: false,
  art_name: false
}

const artSelect = {
  name: true,
  type: true,
  role: true,

  embed_title: true,
  embed_description: true,
  embed_url: true,

  attacks: {
    select: attackSelect
  },
  
  created_at: true,
  updated_at: true,

  guild_id: false
}

async function getAll(logOptions?: LogSettings): Promise<Art[]> {
  const settings = { functionName: 'getAll', ...logOptions }
  
  try {
    const arts = await client.art.findMany({
      select: artSelect
    })

    const logMessage = logMessages['successOnGetAll']
    logger.info(logMessage(), settings)

    return arts;
  } catch {
    const logMessage = logMessages['dataBaseError']
    logger.error(logMessage(), { settings })

    const error = errors['dataBaseError']
    throw error();
  }
}

async function getAllFromGuild(guild_id: string, logOptions?: LogSettings): Promise<Art[]> {
  const settings = { functionName: 'getAllFromGuild', ...logOptions }

  try {
    const arts = await client.art.findMany({
      where: {
        guild_id
      },
      select: artSelect
    })

    const logMessage = logMessages['successOnGetAllFromGuild']
    logger.info(logMessage(guild_id), settings)
    
    return arts;
  } catch {
    const logMessage = logMessages['dataBaseError']
    logger.error(logMessage(), { settings })

    const error = errors['dataBaseError']
    throw error();
  }
}


async function getArtsFromType<Type extends ArtType>(type: Type, logOptions?: LogSettings): Promise<Art[]> {
  const settings = { functionName: 'getArtsFromType<Type>', ...logOptions }
  
  try {
    const arts = await client.art.findMany({
      where: {
        type
      },
      select: artSelect
    })

    const logMessage = logMessages['successOnGetAllFromType']
    logger.info(logMessage(type), settings)

    return arts;
  } catch {
    const logMessage = logMessages['dataBaseError']
    logger.error(logMessage(), { settings })

    const error = errors['dataBaseError']
    throw error();
  }
}


async function getArtsFromGuildAndType<Type extends ArtType>(guild_id: string, type: Type, logOptions?: LogSettings): Promise<Art[]> {
  const settings = { functionName: 'getArtsFromGuildAndType<Type>', ...logOptions }
  
  try {
    const arts = await client.art.findMany({
      where: {
        guild_id,
        type
      },
      select: artSelect
    })

    const logMessage = logMessages['successOnGetAllFromGuildAndType']
    logger.info(logMessage(guild_id, type), settings)

    return arts;
  } catch {
    const logMessage = logMessages['dataBaseError']
    logger.error(logMessage(), { settings })

    const error = errors['dataBaseError']
    throw error();
  }
}

async function getArtFromType<Type extends ArtType>(props: { name: string, guild_id: string, type: Type }, logOptions?: LogSettings): Promise<Art> {
  const settings = { functionName: 'getArtFromType<Type>', ...logOptions}
  
  const { name, guild_id, type } = valid<{ name: string, guild_id: string, type: ArtType }>(props, {
    name: required(),
    guild_id: required(),
    type: { option: required(), allow: ["ATTACK", "RESPIRATION", "KEKKIJUTSU"] }
  })

  let art: Art;

  try {
    art = await client.art.findFirst({
      where: {
        name: { contains: name, mode: 'insensitive' },
        guild_id
      },
      select: artSelect
    })
  } catch(err) {
    console.error(err)

    const logMessage = logMessages['dataBaseError']
    logger.error(logMessage(), { settings })

    const error = errors['dataBaseError']
    throw error();
  }

  if(!art) {
    const logMessage = logMessages['errorOnGetArtFromType']
    logger.error(logMessage(guild_id, { name, type }), { settings })

    const error = errors['artNotExists']
    throw error(guild_id, { name, type });
  }

  const logMessage = logMessages['successOnGetArtFromGuildTypeAndName']
  logger.info(logMessage(guild_id, art), settings)

  return art;
}

async function createArt(art: {
  name: string,
  role?: string | null,
  type: ArtType

  guild_id: string

  embed_title?: string | null,
  embed_description?: string | null,
  embed_url?: string | null
}, logOptions?: LogSettings): Promise<Art> {
  const settings = { functionName: 'createArt', ...(logOptions??{}) }
  
  const data = valid<OriginalArt>(art, {
    name: required(),
    type: required(),
    role: { option: optional(), default: null, allow: null },

    embed_title: { option: optional(), default: null, allow: null },
    embed_description: { option: optional(), default: null, allow: null },
    embed_url: { option: optional(), default: null, allow: null }
  })

  try {
    const art = await client.art.create({ data: {...data}, select: artSelect }) as any

    const logMessage = logMessages['successOnCreateArt']
    logger.info(logMessage(art.guild_id, art), settings)
    
    return art;
  } catch {
    const logMessage = logMessages['errorOnCreateArt']
    logger.error(logMessage(art.guild_id, { name: art.name, type: art.type }), { settings })

    const error = errors['artAlreadyExists']
    throw error(data.guild_id, data)
  }
}

async function editArt(guild_id: string, art: Art, to: {
  name?: string
  role?: string | null

  embed_title?: string | null
  embed_description?: string | null
  embed_url?: string | null
}, logOptions?: LogSettings): Promise<Art> {
  const settings = { functionName: 'getArtFromType<Type>', ...(logOptions??{})}

  const [ name, type ] = [ art.name, art.type ]
  
  const data = valid<{
    name: string
    role: string | null

    embed_title: string | null
    embed_description: string | null
    embed_url: string | null
  }>(to, {
    name: { option: optional(), default: art.name },
    role: { option: optional(), default: art.role, allow: null },

    embed_title: { option: optional(), default: art.embed_title, allow: null },
    embed_description: { option: optional(), default: art.embed_description, allow: null },
    embed_url: { option: optional(), default: art.embed_url, allow: null }
  })
  
  let editedArt: Art;
  
  try {
    editedArt = await client.art.update({ data, where: { name_guild_id: { guild_id, name } }, select: artSelect }) as any
  } catch {
    const logMessage = logMessages['dataBaseError']
    logger.error(logMessage(), { settings })

    const error = errors['dataBaseError']
    throw error();
  }

  if(!editedArt) {
    const logMessage = logMessages['errorOnGetArtFromType']
    logger.error(logMessage(guild_id, { name, type }), { settings })
    
    const error = errors['artNotExists']
    throw error(guild_id, { name, type });
  }

  const logMessage = logMessages['successOnEditArt']
  logger.info(logMessage(guild_id, art), settings)

  return editedArt;
}

export async function deleteArt(art: Art, logOptions?: LogSettings): Promise<Art> {
  const settings = { functionName: 'getArtFromType<Type>', ...(logOptions??{})}
  
  const { name, type, guild_id } = valid<any>(art, {
    name: required(),
    type: { option: required(), allow: ["ATTACK", "RESPIRATION", "KEKKIJUTSU"] },
    role: required(),

    guild_id: required(),

    embed_title: required(),
    embed_description: required(),
    embed_url: required()
  })

  let deletedArt: Art;
  
  try {
    deletedArt = await client.art.delete({
      where: {
        name_guild_id: { guild_id, name }
      },
      select: artSelect
    })
  } catch {
    const logMessage = logMessages['dataBaseError']
    logger.error(logMessage(), { settings })

    const error = errors['dataBaseError']
    throw error();
  }

  if(!deletedArt) {
    const logMessage = logMessages['errorOnGetArtFromType']
    logger.error(logMessage(guild_id, { name, type }), { settings })
    
    const error = errors['artNotExists']
    throw error(guild_id, { name, type });
  }


  const logMessage = logMessages['successOnDeleteArt']
  logger.info(logMessage(guild_id, art), settings)

  return deletedArt;
}

export async function getRespirations(logOptions?: LogSettings): Promise<Respiration[]> {
  return await getArtsFromType("RESPIRATION", { functionName: 'getRespirations', ...logOptions });
}

export async function getRespiration(guild_id: string, name: string, logOptions?: LogSettings): Promise<Respiration> {
  return await getArtFromType({ name, guild_id, type: "RESPIRATION" }, { functionName: 'getRespiration', ...logOptions });
}

export async function getRespirationsFromGuild(guild_id: string, logOptions?: LogSettings): Promise<Respiration[]> {
  return await getArtsFromGuildAndType(guild_id, "RESPIRATION", { functionName: 'getRespirationsFromGuild', ...logOptions });
}

export async function getKekkijutsus(logOptions?: LogSettings): Promise<Kekkijutsu[]> {
  return await getArtsFromType("KEKKIJUTSU", { functionName: 'getKekkijutsus', ...logOptions });
}

export async function getKekkijutsu(guild_id: string, name: string, logOptions?: LogSettings): Promise<Kekkijutsu> {
  return await getArtFromType({ guild_id, name, type: "KEKKIJUTSU" }, { functionName: 'getKekkijutsu', ...logOptions });
}

export async function getKekkijutsusFromGuild(guild_id: string, logOptions?: LogSettings): Promise<Kekkijutsu[]> {
  return await getArtsFromGuildAndType(guild_id, "KEKKIJUTSU" , { functionName: 'getKekkijutsusFromGuild', ...logOptions });
}

export async function createRespiration({
  name,
  role = null,

  guild_id,
  
  embed_title = null,
  embed_description = null,
  embed_url = null
}, logOptions?: LogSettings): Promise<Respiration> {
  return await createArt({
    name: name,
    type: "RESPIRATION",
    role: role,

    guild_id: guild_id,

    embed_title: embed_title,
    embed_description: embed_description,
    embed_url: embed_url
  }, { functionName: 'createRespirations', ...logOptions })
}

export async function createKekkijutsu({
  name,
  role = null,

  guild_id,
  
  embed_title = null,
  embed_description = null,
  embed_url = null
}, logOptions?: LogSettings): Promise<Kekkijutsu> {
  return await createArt({
    name: name,
    type: "KEKKIJUTSU",
    role: role,

    guild_id: guild_id,

    embed_title: embed_title,
    embed_description: embed_description,
    embed_url: embed_url
  }, { functionName: 'createKekkijutsu', ...logOptions })
}

export async function editRespiration(guild_id: string, resp: Respiration, to: {
  name?: string
  role?: string | null

  embed_title?: string | null
  embed_description?: string | null
  embed_url?: string | null
}, logOptions?: LogSettings): Promise<Respiration> {
  return await editArt(guild_id, { ...resp, type: "RESPIRATION" }, to, { functionName: 'editRespiration', ...logOptions })
}
export async function editKekkijutsu(guild_id: string, kekki: Kekkijutsu, to: {
  name?: string
  role?: string | null

  embed_title?: string | null
  embed_description?: string | null
  embed_url?: string | null
}, logOptions?: LogSettings): Promise<Kekkijutsu> {
  return await editArt(guild_id, { ...kekki, type: "KEKKIJUTSU" }, to, { functionName: 'editKekkijutsu', ...logOptions })
}

export const deleteRespiration = async (resp: Respiration) => await deleteArt({...resp, type: "RESPIRATION"}, { functionName: 'deleteRespiration', art_type: 'Respiration' })

export const deleteKekkijutsu = async (kekki: Kekkijutsu) => await deleteArt({...kekki, type: "KEKKIJUTSU"},{ functionName: 'deleteKekkijutsu', art_type: 'Kekkijutsu' })

export default Object.freeze({
  getAll,
  getAllFromGuild,
  getRespirations,
  getRespiration,
  getRespirationsFromGuild,
  getKekkijutsus,
  getKekkijutsu,
  getKekkijutsusFromGuild,

  createRespiration,
  createKekkijutsu,

  editRespiration,
  editKekkijutsu,

  deleteRespiration,
  deleteKekkijutsu
})