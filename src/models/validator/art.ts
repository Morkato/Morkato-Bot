import {
  ValidationError
} from 'errors'

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

export type ArtType = "RESPIRATION" | "KEKKIJUTSU"
export type Art<Type extends ArtType> = {
  name: string
  type: Type
  role: string | null

  embed_title: string | null
  embed_description: string | null
  embed_url: string | null

  attacks: Attack[]

  created_at: Date
  updated_at: Date
}

export type editeArt<Type extends ArtType> = Partial<Omit<Art<Type>, 'attacks' | 'created_at' | 'updated_at'>>

export interface Respiration extends Art<"RESPIRATION"> {  }
export interface Kekkijutsu extends Art<"KEKKIJUTSU"> {  }

export interface editeRespiration extends editeArt<"RESPIRATION"> {  }
export interface editeKekkijutsu extends editeArt<"KEKKIJUTSU"> {  }

const allowedTypes = ['RESPIRATION', 'KEKKIJUTSU']

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
    id: makeContext(Joi.string().trim().regex(/^[0-9]+$/), required['id'], original['id']),

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
  
    embed_title: makeContext(Joi.string().trim().min(1).max(96), required['embed_title'], original['embed_title']),
    embed_description: makeContext(Joi.string().trim().min(1).max(4096), required['embed_description'], original['embed_description']),
    embed_url: makeContext(Joi.string().trim().regex(/^(https?:\/\/|cdn:\/)[^\d \n\t\v\r\f\b]+$/), required['embed_url'], original['embed_url']),
  
    fields: makeContext(Joi.array().items(attackFieldSchema(attackFieldParams)), required['fields'], original['fields']),
    
    created_at: makeContext(Joi.date().allow(Joi.string()), required['created_at'], original['created_at']),
    updated_at: makeContext(Joi.date().allow(Joi.string()), required['updated_at'], original['updated_at'])
  })
}

export function artSchema({ original = {}, required = {}, attackParams = {} }: {
  original?: Partial<Art<ArtType>>,
  required?: Partial<Record<keyof Art<ArtType>, boolean>>,
  attackParams?: Parameters<typeof attackSchema>[0]
}) {
  return Joi.object({
    name: makeContext(Joi.string().trim().min(1).max(32), required['name'], original['name']),
    type: makeContext(Joi.string().valid(...allowedTypes), required['type'], original['type']),
    role: makeContext(Joi.string().allow(null).trim().regex(/^[0-9]+$/), required['role'], original['role']),

    embed_title: makeContext(Joi.string().allow(null).trim().min(1).max(96), required['embed_title'], original['embed_title']),
    embed_description: makeContext(Joi.string().allow(null).trim().min(1).max(4096), required['embed_description'], original['embed_description']),
    embed_url: makeContext(Joi.string().allow(null).trim().regex(/^(https?:\/\/|cdn:\/)[^\d \n\t\v\r\f]+$/), required['embed_url'], original['embed_url']),

    attacks: makeContext(Joi.array().items(attackSchema(attackParams)), required['attacks'], original['attacks']),

    created_at: makeContext(Joi.date().allow(Joi.string()), required['created_at'], original['created_at']),
    updated_at: makeContext(Joi.date().allow(Joi.string()), required['updated_at'], original['updated_at'])
  })
}

export default function validate(obj: unknown, options: Parameters<typeof artSchema>[0]) {
  try {
    obj = JSON.parse(JSON.stringify(obj))
  } catch {
    throw new ValidationError({ message: "O body tem que ser um Json.", action: "Tente enviar um Json dessa vez." });
  }

  const schema = artSchema(options)

  const { value, error } = schema.validate(obj)

  if(error) {
    throw new ValidationError({
      message: error.details[0].message,
      key: error.details[0].context.key || error.details[0].context.type || 'object',
      errorLocationCode: 'MODEL:VALIDATOR:SCHEMA',
      type: error.details[0].type
    });
  }

  return value;
}

export function validateArt(obj: unknown): Art<ArtType> {
  return validate(obj, {
    required: {
      name: true,
      type: true,
      role: true,

      embed_title: true,
      embed_description: true,
      embed_url: true,

      attacks: true,

      created_at: true,
      updated_at: true
    },
    attackParams: {
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
    }
  });
}

export function isValidArt(obj: unknown): obj is Art<ArtType> {
  try {
    return !!validateArt(obj);
  } catch {
    return false;
  }
}