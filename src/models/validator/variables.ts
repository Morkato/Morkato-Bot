import type { Guild } from 'models/guild'

import { makeContext, assert } from './utils'

import Joi from 'joi'

export type Variable = {
  name:                             string
  text:                             string
  visibleCaseIfNotAuthorizerMember: boolean

  required_roles: number
  roles:          string[]

  created_at: Date
  updated_at: Date
}

export function variableSchema({ original = {}, required = {} }: { original?: Partial<Variable>, required?: Partial<Record<keyof Variable, boolean>>}) {
  return Joi.object({
    name: makeContext(Joi.string().trim().min(1).regex(/^[^-+>@&$][a-z0-9_]+[^-+>@&$]$/i), required['name'], original['name']),
    text: makeContext(Joi.string().trim().min(1).max(1024), required['text'], original['text']),
    visibleCaseIfNotAuthorizerMember: makeContext(Joi.boolean(), required['visibleCaseIfNotAuthorizerMember'], original['visibleCaseIfNotAuthorizerMember']),

    required_roles: makeContext(Joi.number().integer(), required['required_roles'], original['required_roles']),
    roles: makeContext(Joi.array().items(Joi.string().regex(/^[0-9]+$/)), required['roles'], original['roles']),

    created_at: makeContext(Joi.date().allow(Joi.string()), required['created_at'], original['created_at']),
    updated_at: makeContext(Joi.date().allow(Joi.string()), required['updated_at'], original['updated_at'])
  })
}

export default function validate<T = Record<string, any>>(obj: Record<string, unknown>, options: Parameters<typeof variableSchema>[0]): T {
  return assert(variableSchema(options), obj) as T;
}

export function assertVariable(obj: Record<string, unknown>): Variable {
  return validate(obj, {
    required: {
      name: true,
      text: true,
      visibleCaseIfNotAuthorizerMember: true,

      required_roles: true,
      roles: true,

      created_at: true,
      updated_at: true
    }
  })
}