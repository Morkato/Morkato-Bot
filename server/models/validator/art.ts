import { makeContext, assert } from './utils'

import { id as guild_id } from './guild'

import Joi from 'joi'

export type ArtType = "RESPIRATION" | "KEKKIJUTSU" | 'FIGHTING_STYLE'
export type Art = {
  name: string
  type: ArtType
  id:   string

  embed_title: string | null
  embed_description: string | null
  embed_url: string | null

  guild_id: string

  created_at: Date
  updated_at: Date
}

const orderBy = { created_at: 'asc' }
const allowedTypes = ['RESPIRATION', 'KEKKIJUTSU', 'FIGHTING_STYLE']

const baseSchemas = {
  name: Joi.string().trim().min(1).max(32).regex(/^[^-+>@&$].+[^-+>@&$]$/),
  type: Joi.string().trim().valid(...allowedTypes),
  id: Joi.string().regex(/^[0-9]+$/),

  embed_title: Joi.string().allow(null).trim().min(1).max(96),
  embed_description: Joi.string().allow(null).trim().min(1).max(4096),
  embed_url: Joi.string().allow(null).trim(),

  guild_id,

  created_at: Joi.date().allow(Joi.string()),
  updated_at: Joi.date().allow(Joi.string())
}

export function artSchema({ original = {}, required = {} }: {
  original?: Partial<Art>,
  required?: Partial<Record<keyof Art, boolean>>
}) {
  return Joi.object({
    name: makeContext(baseSchemas.name, required['name'], original['name']),
    type: makeContext(baseSchemas.type, required['type'], original['type']),
    id: makeContext(baseSchemas.id, required['id'], original['id']),

    embed_title: makeContext(baseSchemas.embed_title, required['embed_title'], original['embed_title']),
    embed_description: makeContext(baseSchemas.embed_description, required['embed_description'], original['embed_description']),
    embed_url: makeContext(baseSchemas.embed_url, required['embed_url'], original['embed_url']),

    guild_id: makeContext(baseSchemas.guild_id, required['guild_id'], original['guild_id']),

    created_at: makeContext(baseSchemas.created_at, required['created_at'], original['created_at']),
    updated_at: makeContext(baseSchemas.updated_at, required['updated_at'], original['updated_at'])
  })
}

export default function validate<T = Record<string, any>>(obj: Record<string, unknown>, options: Parameters<typeof artSchema>[0]) {
  return assert(artSchema(options), obj) as T;
}

export function assertArt(obj: Record<string, unknown>): Art {
  return validate(obj, {
    required: {
      name: true,
      type: true,
      id: true,

      embed_title: true,
      embed_description: true,
      embed_url: true,

      guild_id: true,

      created_at: true,
      updated_at: true
    },
  });
}

export function isValidArt(obj: Record<string, unknown>): obj is Art {
  try {
    return !!assertArt(obj);
  } catch {
    return false;
  }
}

export const {
  name,
  type,
  id,

  embed_title,
  embed_description,
  embed_url,

  created_at,
  updated_at
} = baseSchemas

export { validate };