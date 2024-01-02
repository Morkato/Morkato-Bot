import Joi from 'joi'

import {
  ValidationError
} from 'errors/index'

export const schemas = {
  ids: Joi.array().items(Joi.string().regex(/^[0-9]+$/)).required(),
  id: Joi.string().regex(/^[0-9]+$/).required(),
  art_type: Joi.string().valid('RESPIRATION', 'KEKKIJUTSU', 'FIGHTING_STYLE').required()
}

export function assert<T>(
  schema: Joi.AnySchema<T>,
  obj: T
) {
  try {
    obj = JSON.parse(JSON.stringify(obj))
  } catch {
    throw new ValidationError({ message: "O body tem que ser um Json.", action: "Tente enviar um Json dessa vez." });
  }

  const { value, error } = schema.validate(obj)

  if (error) {
    throw new ValidationError({
      message: error.details[0].message,
      key: error.details[0]?.context?.key || error.details[0]?.context?.type || 'object',
      errorLocationCode: 'MODEL:VALIDATOR:SCHEMA',
      type: error.details[0].type
    });
  }

  return value;
}