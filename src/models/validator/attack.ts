import { makeContext, assert } from './utils'

import { id as guild_id } from './guild'
import { id as art_id }   from './art'

import Joi from 'joi'

export type Attack = {
  name: string
  id:   string

  required_exp: number

  embed_title: string | null
  embed_description: string | null
  embed_url: string | null

  guild_id:  string
  art_id:    string
  parent_id: string

  created_at: Date
  updated_at: Date
}

const baseSchemas = {
  name: Joi.string().trim().min(1).max(32).regex(/^[^-+>@&$].+[^-+>@&$]$/),
  id:   Joi.string().trim().regex(/^[0-9]+$/),

  required_exp: Joi.number().integer(),

  embed_title: Joi.string().allow(null).trim().min(1).max(96),
  embed_description: Joi.string().allow(null).trim().min(1).max(4096),
  embed_url: Joi.string().allow(null).trim(),

  guild_id,
  art_id: art_id.allow(null),
  parent_id: Joi.string().trim().regex(/^[0-9]+$/).allow(null),

  created_at: Joi.date().allow(Joi.string()),
  updated_at: Joi.date().allow(Joi.string())
}

export function attackSchema({ original = {}, required = {} }: {
  original?: Partial<Attack>,
  required?: Partial<Record<keyof Attack, boolean>>
}) {
  return Joi.object({
    name: makeContext(baseSchemas.name, required['name'], original['name']),
    id: makeContext(baseSchemas.id, required['id'], original['id']),
  
    required_exp: makeContext(baseSchemas.required_exp, required['required_exp'], original['required_exp']),
  
    embed_title: makeContext(baseSchemas.embed_title, required['embed_title'], original['embed_title']),
    embed_description: makeContext(baseSchemas.embed_description, required['embed_description'], original['embed_description']),
    embed_url: makeContext(baseSchemas.embed_url, required['embed_url'], original['embed_url']),

    guild_id: makeContext(baseSchemas.guild_id, required['guild_id'], original['guild_id']),
    art_id:  makeContext(baseSchemas.art_id, required['art_id'], original['art_id']),
    parent_id:  makeContext(baseSchemas.parent_id, required['parent_id'], original['parent_id']),
    
    created_at: makeContext(baseSchemas.created_at, required['created_at'], original['created_at']),
    updated_at: makeContext(baseSchemas.updated_at, required['updated_at'], original['updated_at'])
  })
}

export default function validate<T extends Record<string, unknown>>(obj: Record<string, unknown>, options: Parameters<typeof attackSchema>[0]) {
  return assert(attackSchema(options), obj) as T;
}

export function assertAttack(obj: Record<string, unknown>): Attack {
  return validate(obj, {
    required: {
      name: true,
      id: true,

      required_exp: true,

      embed_title: true,
      embed_description: true,
      embed_url: true,

      guild_id: true,
      art_id: true,
      parent_id: true,

      created_at: true,
      updated_at: true
    }
  });
}

export function isValidAttack(obj: Record<string, unknown>): obj is Attack {
  try {
    return !!assertAttack(obj);
  } catch {
    return false;
  }
}

export const {
  name,
  id,

  required_exp,

  embed_title,
  embed_description,
  embed_url,

  parent_id,

  created_at,
  updated_at
} = baseSchemas

export { guild_id, art_id };
export { validate };