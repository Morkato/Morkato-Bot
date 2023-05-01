import valid, { required, optional } from '@/models/validator'
import { NotFoundError } from '@/erros/index'

import query from '@/infra/database'
import Logger from 'infra/logger'

const logger = Logger({
  appName: "models:arts",
  registryLog: true,
  format: '$date $app: $message'
})

export interface Art<Type extends number = 0> {
  name: string
  type: Type
  role: string | null

  guild_id: string

  embed_title: string | null
  embed_description: string | null
  embed_url: string | null

  created_at: Date
  updated_at: Date
}

export interface Respiration extends Art<1> {  }

export interface Kekkijutsu extends Art<2> {  }

export interface NotDefenedArt extends Art<0 | 1 | 2> {  }

async function getAll(): Promise<NotDefenedArt[]> {
  const expcted = {
    text: `
      SELECT
        *
      FROM
        arts
    ;`
  }

  const resuslts = await query(expcted)

  return resuslts.rows;
}
async function getAllFromGuild(guild_id: string): Promise<NotDefenedArt[]> {
  const expcted = {
    text: `
      SELECT
        *
      FROM
        arts
      WHERE
        guild_id = $1
    ;`,
    values: [guild_id]
  }

  const resuslts = await query(expcted)

  return resuslts.rows;
}

async function getArtsFromType<T extends number>(type: T): Promise<Art<T>[]> {
  const expcted = {
    text: `
      SELECT
        *
      FROM
        arts
      WHERE
        type = $1
    ;`,
    values: [type]
  }

  const results = await query(expcted)

  return results.rows;
}

async function getArtsFromGuildAndType<T extends number>(guild_id: string, type: T): Promise<Art<T>[]> {
  const expcted = {
    text: `
      SELECT
        *
      FROM
        arts
      WHERE
        guild_id = $1
        AND type = $2
    ;`,
    values: [guild_id, type]
  }

  const results = await query(expcted)

  return results.rows;
}

async function getArtFromType<T extends number>(props: { name: string, guild_id: string, type: T }): Promise<Art<T>> {
  const { name, guild_id, type } = valid<Art<T>>(props, {
    name: required(),
    guild_id: required(),
    type: { option: required(), allow: [0, 1, 2] }
  })
  const expcted = {
    text: `
      SELECT
        *
      FROM
        arts
      WHERE
        guild_id = $1
        AND LOWER(name) = LOWER($2)
        AND type = $3
      LIMIT
        1
    ;`,
    values: [guild_id, name, type]
  }

  const results = await query(expcted)

  if(results.rowCount === 0)
    throw new NotFoundError({ message: "Art type: " + type + " not exists in guild_id \"" + guild_id + "\"." });

  return results.rows[0];
}

async function createArt<T extends number>(art: {
  name: string,
  role?: string | null,
  type: T

  guild_id: string,

  embed_title?: string | null,
  embed_description?: string | null,
  embed_url?: string | null
}): Promise<Art<T>> {
  const { 
    name,
    type,
    role,
    guild_id,
    embed_title,
    embed_description,
    embed_url
  } = valid<Art<T>>(art, {
    name: required(),
    type: required(),
    role: { option: optional(), default: null, allow: null },

    guild_id: required(),

    embed_title: { option: optional(), default: null, allow: null },
    embed_description: { option: optional(), default: null, allow: null },
    embed_url: { option: optional(), default: null, allow: null }
  })

  const expcted = {
    text: `
      INSERT
        INTO arts (
          name,
          type,
          role,
          guild_id,
          embed_title,
          embed_description,
          embed_url
        ) VALUES (
          $1,
          $2,
          $3,
          $4,
          $5,
          $6,
          $7
        ) RETURNING
          *
    ;`,
    values: [
      name,
      type,
      role,
      guild_id,
      embed_title,
      embed_description,
      embed_url
    ]
  }

  try {
    const results = await query(expcted)
    const art: Art<T> = results.rows[0]

    logger.info(`Created new Art name: ${art.name} of guild id: ${art.guild_id}.`, {})
    
    return art;
  } catch(err) {
    throw err;
  }
}

async function editArt<T extends number>(art: Art<T>, to: {
  name?: string
  role?: string | null

  embed_title?: string | null
  embed_description?: string | null
  embed_url?: string | null
}): Promise<Art<T>> {
  const [ original_name, type, guild_id ] = [ art.name, art.type, art.guild_id ]
  
  const { name, role, embed_title, embed_description, embed_url } = valid<Art<T>>(to, {
    name: { option: optional(), default: art.name },
    role: { option: optional(), default: art.role, allow: null },
    type: { option: optional(), default: art.type, allow: art.type },

    guild_id: { option: optional(), default: art.guild_id, allow: art.guild_id },

    embed_title: { option: optional(), default: art.embed_title, allow: null },
    embed_description: { option: optional(), default: art.embed_description, allow: null },
    embed_url: { option: optional(), default: art.embed_url, allow: null }
  })
  
  const expcted = {
    text: `
      UPDATE
        arts
      SET
        name = $2,
        role = $4,

        embed_title = $6,
        embed_description = $7,
        embed_url = $8,

        updated_at = (NOW())
      WHERE
        guild_id = $5
        AND LOWER(name) = LOWER($1)
        AND type = $3
      RETURNING
        *
    ;`,
    values: [original_name, name, type, role, guild_id, embed_title, embed_description, embed_url]
  }

  const results = await query(expcted)

  art = results.rows[0]

  logger.info(`Art name: ${art.name} edited of guild id: ${art.guild_id}.`, {})

  return art;
}

export async function deleteArt<T extends number>(art: Art<T>): Promise<void> {
  const { name, type, guild_id } = valid<Art<T>>(art, {
    name: required(),
    type: { option: required(), allow: [0, 1, 2] },
    role: required(),

    guild_id: required(),

    embed_title: required(),
    embed_description: required(),
    embed_url: required()
  })
  const expected = {
    text: `
      DELETE FROM
        arts
      WHERE
        guild_id = $1
        AND type = $2
        AND LOWER(name) = LOWER($3)
    ;`,
    values: [guild_id, type, name]
  }

  await query(expected)

  logger.info(`Art name: ${name} of guild_id: ${guild_id} deleted.`, {})
}

export async function getRespirations(): Promise<Respiration[]> {
  return await getArtsFromType(1);
}

export async function getRespiration(guild_id: string, name: string): Promise<Respiration> {
  return await getArtFromType({ name, guild_id, type: 1 });
}

export async function getRespirationsFromGuild(guild_id: string): Promise<Respiration[]> {
  return await getArtsFromGuildAndType(guild_id, 1);
}

export async function getKekkijutsus(): Promise<Kekkijutsu[]> {
  return await getArtsFromType(2);
}

export async function getKekkijutsu(guild_id: string, name: string): Promise<Kekkijutsu> {
  return await getArtFromType({ guild_id, name, type: 2 });
}

export async function getKekkijutstsFromGuild(guild_id): Promise<Kekkijutsu[]> {
  return await getArtsFromGuildAndType(guild_id, 2);
}

export async function createRespiration({
  name,
  role = null,

  guild_id,
  
  embed_title = null,
  embed_description = null,
  embed_url = null
}): Promise<Respiration> {
  return await createArt({
    name: name,
    type: 1,
    role: role,

    guild_id: guild_id,

    embed_title: embed_title,
    embed_description: embed_description,
    embed_url: embed_url
  })
}

export async function createKekkijutsu({
  name,
  role = null,

  guild_id,
  
  embed_title = null,
  embed_description = null,
  embed_url = null
}): Promise<Kekkijutsu> {
  return await createArt({
    name: name,
    type: 2,
    role: role,

    guild_id: guild_id,

    embed_title: embed_title,
    embed_description: embed_description,
    embed_url: embed_url
  })
}

export async function editRespiration(resp: Respiration, to: {
  name?: string
  role?: string | null

  embed_title?: string | null
  embed_description?: string | null
  embed_url?: string | null
}): Promise<Respiration> {
  return await editArt({ ...resp, type: 1 }, to)
}
export async function editKekkijutsu(kekki: Kekkijutsu, to: {
  name?: string
  role?: string | null

  embed_title?: string | null
  embed_description?: string | null
  embed_url?: string | null
}): Promise<Kekkijutsu> {
  return await editArt({ ...kekki, type: 2 }, to)
}

export const deleteRespiration = async (resp: Respiration) => await deleteArt({...resp, type: 1})

export const deleteKekkijutsu = async (kekki: Kekkijutsu) => await deleteArt({...kekki, type: 2})

export default Object.freeze({
  getAll,
  getAllFromGuild,
  getRespirations,
  getRespiration,
  getRespirationsFromGuild,
  getKekkijutsus,
  getKekkijutsu,
  getKekkijutstsFromGuild,

  createRespiration,
  createKekkijutsu,

  editRespiration,
  editKekkijutsu,

  deleteRespiration,
  deleteKekkijutsu
})