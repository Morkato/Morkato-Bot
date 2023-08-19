import { Prisma } from '@prisma/client'

import { assert } from './utils'

import Joi from 'joi'

export type Guild = {
  id: string

  created_at: Date
  updated_at: Date
}

export const baseSchemas = {
  id: Joi.string().trim().regex(/^[0-9]+$/),

  created_at: Joi.date().allow(Joi.string()),
  updated_at: Joi.date().allow(Joi.string())
}

function makeContext<T>(schema: Joi.AnySchema<T>, required: boolean, original?: any) {
  if(required) {
    return schema.required();
  }

  if(typeof original !== 'undefined') {
    schema = schema.default(original)
  }

  return schema.optional();
}

export function guildSchema({ original = {}, required = {}} : { original?: Partial<Record<keyof Guild, unknown>>, required?: Partial<Record<keyof Guild, any>>}) {
  return Joi.object({
    id: makeContext(baseSchemas.id, required['id'], original['id']),
    
    created_at: makeContext(baseSchemas.created_at, required['created_at'], original['created_at']),
    updated_at: makeContext(baseSchemas.updated_at, required['updated_at'], original['updated_at'])
  });
}

export default function validate<T>(obj: Record<string, unknown>, options: Parameters<typeof guildSchema>[0]) {
  return assert(guildSchema(options), obj) as T;
}

export function assertGuild(obj: Record<string, unknown>): Guild {
  return validate(obj, {
    required: {
      id: true,

      created_at: true,
      updated_at: true
    }
  });
}

export function isValidGuild(obj: Record<string, unknown>): obj is Guild {
  try {
    return !!assertGuild(obj);
  } catch {
    return false;
  }
}

export const created_at = baseSchemas.created_at
export const updated_at = baseSchemas.updated_at
export const id         = baseSchemas.id