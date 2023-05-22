import { ValidationError } from 'errors'

import Joi from 'joi'

const keys = {
  name: () => Joi.string()
    .trim()
    .regex(/^[\D0-9].+$/)
    .min(1)
    .max(32)
    .when('$required.name', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
    .when('$allow.name', { is: null, then: Joi.allow(null) })
}

type DefaultKeys = typeof keys
type SchemaKeys = keyof DefaultKeys

export function createSchema<Keys extends SchemaKeys[]>(
  rows_keys: Keys,
): Joi.ObjectSchema<Record<Keys[number], ReturnType<DefaultKeys[Keys[number]]>>> {
  return Joi.object(Object.fromEntries(rows_keys.map(key => ([key, (keys[key])()]))))
}

export default function validate<
  Keys extends SchemaKeys[],
  Rows_Keys extends Record<Keys[number], 'required' | 'optional'>,
  Results extends Record<
  Keys[number] | undefined,
  
  Rows_Keys[Keys[number]] extends 'required'
    ? ReturnType<DefaultKeys[Keys[number]]>['type']
    : (undefined) | ReturnType<DefaultKeys[Keys[number]]>['type']>
>(
  obj: Record<string, unknown>,
  keys: Rows_Keys,
  options?: {
    allows?: Record<Keys[number], unknown>,
    defaults?: Record<Keys[number], unknown>
  }
): Results {
  try {
    obj = JSON.parse(JSON.stringify(obj))
  } catch {
    throw new ValidationError({ message: "O body tem que ser um Json.", action: "Tente enviar um Json desssa vez." })
  }

  const schema = createSchema(Object.keys(keys) as Keys)

  const { error, value } = schema.validate(obj, {
    context: {
      required: keys,
      allow: options?.allows || {},
      default: options?.defaults || {}
    }
  })

  if(!error)
    return value as Results;

  throw new ValidationError({
    message: error.details[0].message,
    key: error.details[0].context.key || error.details[0].context.type || 'object',
    errorLocationCode: 'MODEL:VALIDATOR:SCHEMA',
    type: error.details[0].type
  });
}