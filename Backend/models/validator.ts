import utils from 'utils'
import Joi from 'joi'

import {
  ValidationError
} from 'errors'

export function makeContextSchemaField(
  field: Joi.AnySchema,
  original: any,
  required?: boolean
) {
  if(required) {
    return field.required();
  }

  if(original === undefined) {
    field = field.default(original);
  }

  return field.optional();
}

export function makeContextSchema<
  S extends Record<string, Joi.AnySchema> = {},
  Ks extends keyof S = keyof S
>(
  schema: S,
  options?: {
    default?: Partial<Record<Ks, unknown>>
    required?: Partial<Record<Ks, boolean>>
  }
) {
  return Joi.object(utils.object.map(schema, ([key, field]) => makeContextSchemaField(field, options?.default[key], options?.required[key])))
}

export default function validator<T, 
  S extends Record<string, Joi.AnySchema> = {},
  Ks extends keyof S = keyof S
>(
  obj: Record<string, any>,
  schema: S,
  options?: {
    default?: Partial<Record<Ks, unknown>>
    required?: Partial<Record<Ks, boolean>>
  }
): T {
  try {
    obj = JSON.parse(JSON.stringify(obj))
  } catch {
    throw new ValidationError({ message: "O body tem que ser um Json.", action: "Tente enviar um Json dessa vez." })
  }

  const schemaFiltered = makeContextSchema(schema, options)

  const { value, error } = schemaFiltered.validate(obj)

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