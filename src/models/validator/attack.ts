import { assertSchema } from './utils'

import Joi from 'joi'

export type AttackField = {
  id: string

  text: string
  roles: string[]

  created_at: Date
  updated_at: Date
}

export type Attack = {
  name: string

  roles: string[]
  required_roles: number
  required_exp: number

  damage: number
  stamina: number

  embed_title: string | null
  embed_description: string | null
  embed_url: string | null

  fields: AttackField[]

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
    roles: makeContext(Joi.array().items(Joi.string().trim().regex(/^[0-9]+$/)), required['roles'], original['roles']),

    created_at: makeContext(Joi.date().allow(Joi.string()), required['created_at'], original['created_at']),
    updated_at: makeContext(Joi.date().allow(Joi.string()), required['updated_at'], original['updated_at'])
  })
}

export function attackSchema({ original = {}, required = {}, attackFieldParams = {} }: {
  original?: Partial<Attack>,
  required?: Partial<Record<keyof Attack, boolean>>,
  attackFieldParams?: Parameters<typeof attackFieldSchema>[0]
}) {
  return Joi.object({
    name: makeContext(Joi.string().trim().min(1).max(32), required['name'], original['name']),
  
    roles: makeContext(Joi.array().items(Joi.string().trim().regex(/^[0-9]+$/)), required['roles'], original['roles']),
    required_roles: makeContext(Joi.number().integer(), required['required_roles'], original['required_roles']),
    required_exp: makeContext(Joi.number().integer(), required['required_exp'], original['required_exp']),
  
    damage: makeContext(Joi.number().integer(), required['damage'], original['damage']),
    stamina: makeContext(Joi.number().integer(), required['stamina'], original['stamina']),
  
    embed_title: makeContext(Joi.string().allow(null).trim().min(1).max(96), required['embed_title'], original['embed_title']),
    embed_description: makeContext(Joi.string().allow(null).trim().min(1).max(4096), required['embed_description'], original['embed_description']),
    embed_url: makeContext(Joi.string().allow(null).trim(), required['embed_url'], original['embed_url']),
  
    fields: makeContext(Joi.array().items(attackFieldSchema(attackFieldParams)), required['fields'], original['fields']),
    
    created_at: makeContext(Joi.date().allow(Joi.string()), required['created_at'], original['created_at']),
    updated_at: makeContext(Joi.date().allow(Joi.string()), required['updated_at'], original['updated_at'])
  })
}

export default function validate<T>(obj: Record<string, unknown>, options: Parameters<typeof attackSchema>[0]) {
  return assertSchema(attackSchema(options), obj) as T;
}

export function validateAttack(obj: Record<string, unknown>): Attack {
  return validate(obj, {
    required: {
      name: true,
      roles: true,

      required_roles: true,
      required_exp: true,

      damage: true,
      stamina: true,

      embed_title: true,
      embed_description: true,
      embed_url: true,

      fields: true,

      created_at: true,
      updated_at: true
    },
    attackFieldParams: {
      required: {
        id: true,

        text: true,
        roles: true,
        
        created_at: true,
        updated_at: true
      }
    }
  });
}

export function isValidAttack(obj: Record<string, unknown>): obj is Attack {
  try {
    return !!validateAttack(obj);
  } catch {
    return false;
  }
}