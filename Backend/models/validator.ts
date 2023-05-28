import Joi from 'joi'

import {
  ValidationError
} from 'errors'

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

  

}