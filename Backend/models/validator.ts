import utils from 'utils'
import Joi from 'joi'

import {
  ValidationError
} from 'errors'


type PermitSchema = { [key: string]: Joi.AnySchema | PermitSchema }

export function makeContextSchemaField(
  field: Joi.AnySchema,
  original?: any,
  required?: boolean
) {
  if(required) {
    return field.required();
  }

  if(original !== undefined) {
    field = field.default(original);
  }

  return field.optional();
}

export function makeContextSchema<
  S extends PermitSchema = {},
  Ks extends keyof S = keyof S
>(
  schema: S,
  options?: {
    default?: Partial<Record<Ks, { next?: unknown, default?: unknown }>>
    required?: Partial<Record<Ks, boolean | { requiredFields?: unknown, required?: boolean }>>
  }
): Joi.ObjectSchema | Joi.ArraySchema {
  options = options ?? {}

  options.required = options.required ?? {}
  options.default = options.default ?? {}
  
  return Joi.object(utils.object.map(schema, ([key, field]) => {
    const defaultKey = options.default[key] ?? {}
    const requiredKey = (typeof options.required[key] === 'boolean' ? { required: options.required[key] } : options.required[key]) ?? {}

    const next = !!defaultKey.next
    const defaultValue = defaultKey.default

    const required = !!requiredKey.required
    const requiredFields = requiredKey.requiredFields ?? {}

    if(Joi.isSchema(field)) {
      return makeContextSchemaField(field, defaultValue, required);
    }
    
    const schema = makeContextSchema(field, { default: next ? defaultValue : {}, required: requiredFields })

    return makeContextSchemaField(schema, utils.object.map(defaultValue, ([key, value]) => value.default), required);
  }))
}

export function CompileSchema<T>(
  schema: Joi.AnySchema,
  obj: any
): T {
  try {
    obj = JSON.parse(JSON.stringify(obj))
  } catch {
    throw new ValidationError({ message: "O body tem que ser um Json.", action: "Tente enviar um Json dessa vez." })
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

export default function validator<T, S extends PermitSchema = {}
>(
  obj: Record<string, any>,
  schema: S,
  options?: {
    default?: Partial<Record<keyof S, { next?: boolean, default?: unknown }>>
    required?: Partial<Record<keyof S, boolean | { requiredFields?: unknown, required?: boolean }>>
  }
): T {
  return CompileSchema<T>(makeContextSchema(schema, options ?? {}), obj);
}