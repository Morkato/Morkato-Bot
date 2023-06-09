import { Attack, attackSchema } from './attack'

import { makeContext, assert } from './utils'

import Joi from 'joi'

export type ArtType = "RESPIRATION" | "KEKKIJUTSU"
export type Art = {
  name: string
  type: ArtType
  role: string | null

  embed_title: string | null
  embed_description: string | null
  embed_url: string | null

  attacks: Attack[]

  created_at: Date
  updated_at: Date
}

export type editeArt = Partial<Omit<Art, 'attacks' | 'created_at' | 'updated_at'>>

const allowedTypes = ['RESPIRATION', 'KEKKIJUTSU']

export function artSchema({ original = {}, required = {}, attackParams = {} }: {
  original?: Partial<Art>,
  required?: Partial<Record<keyof Art, boolean>>,
  attackParams?: Parameters<typeof attackSchema>[0]
}) {
  return Joi.object({
    name: makeContext(Joi.string().trim().min(1).max(32), required['name'], original['name']),
    type: makeContext(Joi.string().valid(...allowedTypes), required['type'], original['type']),
    role: makeContext(Joi.string().allow(null).trim().regex(/^[0-9]+$/), required['role'], original['role']),

    embed_title: makeContext(Joi.string().allow(null).trim().min(1).max(96), required['embed_title'], original['embed_title']),
    embed_description: makeContext(Joi.string().allow(null).trim().min(1).max(4096), required['embed_description'], original['embed_description']),
    embed_url: makeContext(Joi.string().allow(null).trim(), required['embed_url'], original['embed_url']),

    attacks: makeContext(Joi.array().items(attackSchema(attackParams)), required['attacks'], original['attacks']),

    created_at: makeContext(Joi.date().allow(Joi.string()), required['created_at'], original['created_at']),
    updated_at: makeContext(Joi.date().allow(Joi.string()), required['updated_at'], original['updated_at'])
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
      role: true,

      embed_title: true,
      embed_description: true,
      embed_url: true,

      attacks: true,

      created_at: true,
      updated_at: true
    },
    attackParams: {
      required: {
        name: true,
        roles: true,

        required_roles: true,
        required_exp: true,

        damage: true,
        stamina: true,

        embed_title: true,
        embed_description: true,
        embed_url: true,

        created_at: true,
        updated_at: true
      }
    }
  });
}

export function isValidArt(obj: Record<string, unknown>): obj is Art {
  try {
    return !!assertArt(obj);
  } catch {
    return false;
  }
}