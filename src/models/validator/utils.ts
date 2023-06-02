import Joi from 'joi'

import {
  ValidationError
} from 'errors'

export function assertSchema<T>(
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
      key: error.details[0].context.key || error.details[0].context.type || 'object',
      errorLocationCode: 'MODEL:VALIDATOR:SCHEMA',
      type: error.details[0].type
    });
  }

  return value as T;
}

export const regex = {
  id: /^[0-9]+$/
}

export const schemas = {
  id: Joi.string().regex(regex.id),
  arrayId: Joi.array().items(Joi.string().regex(regex.id)),
  name: Joi.string().trim().min(1).max(32)
}