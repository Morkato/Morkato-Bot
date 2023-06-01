import {
  ValidationError
} from 'errors'

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

export function guildSchema({ original = {}, required = {} } : { original: Partial<Record<keyof Guild, unknown>>, required: Partial<Record<keyof Guild, boolean>> }) {
  return Joi.object({
    id: makeContext(Joi.string().trim().regex(/^[0-0]+$/), required['id'], original['id']),

    created_at: makeContext(Joi.date().allow(Joi.string()), required['created_at'], original['created_at']),
    updated_at: makeContext(Joi.date().allow(Joi.string()), required['updated_at'], original['updated_at'])
  })
}

export default function validate<T>(obj: Record<string, unknown>, options: Parameters<typeof guildSchema>[0]) {
  try {
    obj = JSON.parse(JSON.stringify(obj))
  } catch {
    throw new ValidationError({ message: "O body tem que ser um Json.", action: "Tente enviar um Json dessa vez." });
  }

  const schema = guildSchema(options)

  const { value, error } = schema.validate(obj)

  if(error) {
    throw new ValidationError({
      message: error.details[0].message,
      key: error.details[0].context.key || error.details[0].context.type || 'object',
      errorLocationCode: 'MODEL:VALIDATOR:SCHEMA',
      type: error.details[0].type
    });
  }

  return value as T;
}