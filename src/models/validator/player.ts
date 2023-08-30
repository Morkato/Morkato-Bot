import { makeContext, assert } from './utils'

import { id as guild_id } from './guild'

import Joi from 'joi'

type PlayerBreed = 'HUMAN' | 'ONI' | 'HYBRID'

type Player = {
  guild_id: string
  id:       string
  breed:    PlayerBreed

  name:        string
  credibility: number

  cash: number

  life:   number
  blood:  number
  breath: number
  exp:    number

  appearance:   string | null
}

const baseSchema = {
  guild_id: guild_id,
  id: Joi.string().regex(/^[0-9]+$/),
  breed: Joi.string().valid('HUMAN', 'ONI', 'HYBRID'),

  name: Joi.string().min(2).max(32),
  credibility: Joi.number().integer(),

  cash: Joi.number().integer(),

  life: Joi.number().integer(),
  blood: Joi.number().integer(),
  breath: Joi.number().integer(),
  exp: Joi.number().integer(),

  appearance: Joi.string().allow(null).uri()
}

type AttackWhereSchema = {
  original?: Partial<Player>
  required?: Partial<Record<keyof Player, boolean>>
}

export default function validate<T extends Partial<Player> = {}>(obj: any, options?: AttackWhereSchema) {
  return assert(playerSchema(options??{}), obj) as T;
}

export function playerSchema({ original = {}, required = {} }: AttackWhereSchema) {
  return Joi.object({
    guild_id: makeContext(guild_id, required['guild_id'], original['guild_id']),
    id: makeContext(baseSchema.id, required['id'], original['id']),
    breed: makeContext(baseSchema.breed, required['breed'], original['breed']),

    name: makeContext(baseSchema.name, required['name'], original['name']),
    credibility: makeContext(baseSchema.credibility, required['credibility'], original['credibility']),

    cash: makeContext(baseSchema.cash, required['cash'], original['cash']),

    life: makeContext(baseSchema.life, required['life'], original['life']),
    blood: makeContext(baseSchema.blood, required['blood'], original['blood']),
    breath: makeContext(baseSchema.breath, required['breath'], original['breath']),
    exp: makeContext(baseSchema.exp, required['exp'], original['exp']),

    appearance: makeContext(baseSchema.appearance, required['appearance'], original['appearance'])
  })
}

export const {
  id,
  breed,

  name,
  credibility,

  cash,

  life,
  blood,
  breath,
  exp,

  appearance
} = baseSchema;

export type { Player, PlayerBreed };

export { validate };
export { guild_id };