import Joi from 'joi'

import {
  ValidationError
} from 'errors'

export function assert<T>(
  schema: Joi.AnySchema,
  obj: any
): T {
  try {
    obj = JSON.parse(JSON.stringify(obj))
  } catch {
    throw new ValidationError({ message: "O body tem que ser um Json.", action: "Tente enviar um Json dessa vez." });
  }

  const { value, error } = schema.validate(obj)

  if(error) {
    throw new ValidationError({
      message: error.details[0].message,
      key: error.details[0]?.context?.key || error.details[0]?.context?.type || 'object',
      errorLocationCode: 'MODEL:VALIDATOR:SCHEMA',
      type: error.details[0].type
    });
  }

  return value as T;
}

export function makeContext<T>(schema: Joi.AnySchema<T>, required: boolean | undefined, original?: any) {
  if(required) {
    return schema.required();
  }

  if(typeof original !== 'undefined') {
    schema = schema.default(original)
  }

  return schema.optional();
}

export const regex = {
  id: /^[0-9]+$/
}

export const schemas = {
  id: Joi.string().trim().regex(regex.id),
  uuid: Joi.string().min(1),
  arrayId: Joi.array().items(Joi.string().regex(regex.id)),
  name: Joi.string().trim().min(1).max(32).regex(/^[^-+>@&$].+[^-+>@&$]$/),
  art_type: Joi.string().trim().valid('RESPIRATION', 'KEKKIJUTSU'),
  player_breed: Joi.string().trim().valid('HUMAN', 'ONI', 'HYBRID'),
  player_rank: Joi.string().trim().valid('F', 'E', 'D', 'C', 'B', 'A', 'AA', 'AAA', 'AAAA', 'S', 'SS', 'SSS', 'SSSS'),
  exp: Joi.number().integer(),

  embed_title: Joi.string().trim().allow(null).min(1).max(96),
  embed_description: Joi.string().trim().allow(null).min(1).max(4096),
  embed_url: Joi.string().trim().allow(null).uri(),
  embed_icon: Joi.string().trim().allow(null).uri()
}