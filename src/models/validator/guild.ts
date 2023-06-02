import { assertSchema } from './utils'

import Joi from 'joi'

export type Guild = {
  id: string

  created_at: Date
  updated_at: Date
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

export function guildSchema({ original = {}, required = {} } : { original?: Partial<Record<keyof Guild, unknown>>, required?: Partial<Record<keyof Guild, boolean>> }) {
  return Joi.object({
    id: makeContext(Joi.string().trim().regex(/^[0-9]+$/), required['id'], original['id']),

    created_at: makeContext(Joi.date().allow(Joi.string()), required['created_at'], original['created_at']),
    updated_at: makeContext(Joi.date().allow(Joi.string()), required['updated_at'], original['updated_at'])
  });
}

export default function validate<T>(obj: Record<string, unknown>, options: Parameters<typeof guildSchema>[0]) {
  return assertSchema(guildSchema(options), obj) as T;
}

export function validateGuild(obj: Record<string, unknown>): Guild {
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
    return !!validateGuild(obj);
  } catch {
    return false;
  }
}