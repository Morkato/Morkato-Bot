import valid, { makeContextSchema } from '.'
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

export type ArtType = "RESPIRATION" | "KEKKIJUTSU" | "ATTACK"
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

const allowedTypes = ['ATTACK', 'RESPIRATION', 'KEKKIJUTSU']

export const attackFieldSchema = {
  id: Joi.string().trim().regex(/^[0-9]+$/),

  text: Joi.string().trim().min(1).max(132),
  roles: Joi.array().items(Joi.string().trim().regex(/^[0-9]+$/)),

  created_at: Joi.date().allow(Joi.string()),
  updated_at: Joi.date().allow(Joi.string())
}

export const attackSchema = {
  name: Joi.string().trim().min(1).max(32),

  roles: Joi.array().items(Joi.string().trim().regex(/^[0-9]+$/)),
  required_roles: Joi.number().integer(),
  required_exp: Joi.number().integer(),

  damage: Joi.number().integer(),
  stamina: Joi.number().integer(),

  embed_title: Joi.string().trim().min(1).max(96),
  embed_description: Joi.string().trim().min(1).max(4096),
  embed_url: Joi.string().trim().regex(/^(https?:\/\/|cdn:\/)[^\d \n\t\v\r\f\b]+$/),

  fields: Joi.array().items(Joi.object(attackFieldSchema)),
  
  created_at: Joi.date().allow(Joi.string()),
  updated_at: Joi.date().allow(Joi.string())
}

export const artSchema = <Type extends ArtType>(valid?: Type) => ({
  name: Joi.string().trim().min(1).max(32),
  type: Joi.string().trim().valid(...(allowedTypes.includes(valid) ? [valid,] : allowedTypes)),
  role: Joi.string().trim().regex(/^[0-9]+$/),

  embed_title: Joi.string().trim().min(1).max(96),
  embed_description: Joi.string().trim().min(1).max(4096),
  embed_url: Joi.string().trim().regex(/^(https?:\/\/|cdn:\/)[^\d \n\t\v\r\f\b]+$/),

  attacks: Joi.array().items(Joi.object(attackFieldSchema)),
  
  created_at: Joi.date().allow(Joi.string()),
  updated_at: Joi.date().allow(Joi.string())
})

export function validate<Type extends ArtType>(obj: unknown, type: Type, options: {
  default?: Partial<Record<keyof ReturnType<typeof artSchema<Type>>, { next?: boolean, default: unknown }>>,
  required?: Partial<Record<keyof ReturnType<typeof artSchema<Type>>, boolean | { required?: boolean, requiredFields?: unknown }>>
}): Type extends 'RESPIRATION' ? Respiration : Type extends 'KEKKIJUTSU' ? Kekkijutsu : Art<Type> {
  return valid(obj, artSchema(type), options);
}

export function catchIsValidArt(obj: unknown, type: ArtType) : Art<ArtType> {
  return validate(obj, type, {
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
    }
  })
}