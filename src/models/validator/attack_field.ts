import { assertSchema } from './utils'

import Joi from 'joi'

export type AttackField = {
  id: string

  text: string
  roles: string[]

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

export function attackFieldSchema({ original = {}, required = {} } : {
  original?: Partial<AttackField>,
  required?: Partial<Record<keyof AttackField, boolean>>
}) {
  return Joi.object({
    id: makeContext(Joi.string().trim(), required['id'], original['id']),

    text: makeContext(Joi.string().trim().min(1).max(132), required['text'], original['text']),
    roles: makeContext(Joi.array().items(Joi.string().trim()), required['roles'], original['roles']),

    created_at: makeContext(Joi.date().allow(Joi.string()), required['created_at'], original['created_at']),
    updated_at: makeContext(Joi.date().allow(Joi.string()), required['updated_at'], original['updated_at'])
  })
}

export default function validate<T>(obj: Record<string, unknown>, options: Parameters<typeof attackFieldSchema>[0]) {
  return assertSchema(attackFieldSchema(options), obj) as T;
}

export function validateAttackField(obj: Record<string, unknown>): AttackField {
  return validate(obj, {
    required: {
      id: true,

      text: true,
      roles: true,

      created_at: true,
      updated_at: true
    }
  });
}

export function isValidAttackField(obj: Record<string, unknown>): obj is AttackField {
  try {
    return !!validateAttackField(obj);
  } catch {
    return false;
  }
}