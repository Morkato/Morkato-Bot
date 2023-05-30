import type { Guild } from '../guild'

import Joi from 'joi'
import valid from '.'

const guildSchema = {
  id: Joi.string().regex(/^[0-9]+$/),

  created_at: Joi.date().allow(Joi.string()),
  updated_at: Joi.date().allow(Joi.string())
}

export default function validate(guild: unknown, options?: {
  default?: Partial<Record<keyof typeof guildSchema, { next?: boolean, default: unknown }>>,
  required?: Partial<Record<keyof typeof guildSchema, boolean | { required?: boolean, requiredFields?: unknown }>>
}): Guild {
  return valid(guild, guildSchema, options);
}

export function catchIsValidGuild(guild: unknown): guild is Guild {
  return !!validate(guild, {
    required: {
      id: true,

      created_at: true,
      updated_at: true
    }
  });
}

export function isValidGuild(obj: unknown): obj is Guild {
  try {
    return catchIsValidGuild(obj);
  } catch {
    return false;
  }
}