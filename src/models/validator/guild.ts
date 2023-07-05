import { type Variable, variableSchema } from './variables'

import { assert } from './utils'

import Joi from 'joi'

export type Guild = {
  id: string

  vars: Variable[]

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

export function guildSchema({ original = {}, required = {}, varParams = {}} : { original?: Partial<Record<keyof Guild, unknown>>, required?: Partial<Record<keyof Guild, any>>, varParams?: Parameters<typeof variableSchema>[0] }) {
  return Joi.object({
    id: makeContext(Joi.string().trim().regex(/^[0-9]+$/), required['id'], original['id']),

    vars: makeContext(Joi.array().items(variableSchema(varParams)), required['vars'], original['vars']),
    
    created_at: makeContext(Joi.date().allow(Joi.string()), required['created_at'], original['created_at']),
    updated_at: makeContext(Joi.date().allow(Joi.string()), required['updated_at'], original['updated_at'])
  });
}

export default function validate<T>(obj: Record<string, unknown>, options: Parameters<typeof guildSchema>[0]) {
  return assert(guildSchema(options), obj) as T;
}

export function assertGuild(obj: Record<string, unknown>): Guild {
  return validate(obj, {
    required: {
      id: true,

      vars: true,

      created_at: true,
      updated_at: true
    },
    varParams: {
      required: {
        name: true,
        text: true,
        visibleCaseIfNotAuthorizerMember: true,

        roles: true,
        required_roles: true
      }
    }
  });
}

export function isValidGuild(obj: Record<string, unknown>): obj is Guild {
  try {
    return !!assertGuild(obj);
  } catch {
    return false;
  }
}