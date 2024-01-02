import { ValidationError } from 'errors'

import Joi from 'joi'

function uint() {
  return Joi.number().integer().min(-1).max(4294967295)
}

export function validate(
  object: Record<string, unknown>,
  keys: Partial<Record<keyof typeof schemas, 'required' | 'optional'>>
) {
  try {
    object = JSON.parse(JSON.stringify(object));
  } catch (error) {
    throw new ValidationError({
      message: 'Não foi possível interpretar o valor enviado.',
      action: 'Verifique se o valor enviado é um JSON válido.',
      errorLocationCode: 'MODEL:VALIDATOR:ERROR_PARSING_JSON',
      key: 'object',
    })
  }

  let finalSchema = Joi.object().required().min(1).messages({
    'object.base': `Body enviado deve ser do tipo Object.`,
    'object.min': `Objeto enviado deve ter no mínimo uma chave.`,
  })

  for (const key of Object.keys(keys)) {
    const callback = schemas[key]
    finalSchema.concat(callback())
  }

  const { error, value } = finalSchema.validate(object, {
    stripUnknown: true,
    context: {
      required: keys
    }
  })

  if (error) {
    throw new ValidationError({
      message: error.details[0].message,
      key: error.details[0]?.context?.key || error.details[0]?.context?.type || 'object',
      errorLocationCode: 'MODEL:VALIDATOR:FINAL_SCHEMA',
      type: error.details[0].type,
    })
  }

  return value;
}

export const schemas = {
  exclude: () => Joi.object({
    exclude: Joi.boolean()
  }),
  add: () => Joi.object({
    add: uint()
  }),
  remove: () => Joi.object({
    remove: uint()
  }),
  name: () => Joi.object({
    name: Joi.string()
      .trim()
      .min(3)
      .max(32)
      .regex(/^[^-+>@&$\s].+[^-+>@&$\s]$/)
      .when('$required.name', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  description: () => Joi.object({
    description: Joi.string()
      .trim()
      .allow(null)
      .min(1)
      .max(4096)
      .when('$required.description', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  breed: () => Joi.object({
    breed: Joi.string()
      .trim()
      .valid('HUMAN', 'ONI', 'HYBRID')
      .when('$required.breed', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  history: () => Joi.object({
    history: Joi.string()
      .trim()
      .min(2)
      .max(2048)
      .regex(/^[^\s].*[^\s]$/)
  }),
  id: () => Joi.object({
    id: Joi
      .string()
      .min(6)
      .regex(/^[0-9]+$/)
      .when('$required.id', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  guild_id: () => Joi.object({
    guild_id: Joi
      .string()
      .min(6)
      .regex(/^[0-9]+$/)
      .when('$required.guild_id', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  art_id: () => Joi.object({
    art_id: Joi
      .string()
      .min(6)
      .regex(/^[0-9]+$/)
      .when('$required.art_id', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  item_id: () => Joi.object({
    item_id: Joi
      .string()
      .min(6)
      .regex(/^[0-9]+$/)
      .when('$required.item_id', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  player_id: () => Joi.object({
    player_id: Joi
      .string()
      .min(6)
      .regex(/^[0-9]+$/)
      .when('$required.player_id', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  art_type: () => Joi.object({
    type: Joi.string()
      .trim()
      .valid('RESPIRATION', 'KEKKIJUTSU', 'FIGHTING_STYLE')
      .when('$required.art_type', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  parent_id: () => Joi.object({
    parent_id: Joi
      .string()
      .min(6)
      .regex(/^[0-9]+$/)
      .when('$required.parent_id', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  role: () => Joi.object({
    role: Joi.string()
      .min(6)
      .regex(/^[0-9]+$/)
      .when('$required.role', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  required_exp: () => Joi.object({
    required_exp: uint()
      .when('$required.required_exp', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  credibility: () => Joi.object({
    credibility: uint()
      .when('$required.credibility', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  damage: () => Joi.object({
    damage: uint()
      .when('$required.damage', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  life: () => Joi.object({
    life: uint()
      .when('$required.life', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  breath: () => Joi.object({
    breath: uint()
      .when('$required.breath', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  blood: () => Joi.object({
    blood: uint()
      .when('$required.blood', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  cash: () => Joi.object({
    cash: uint()
      .when('$required.cash', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  exp: () => Joi.object({
    exp: uint()
      .when('$required.exp', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  force: () => Joi.object({
    force: uint()
      .when('$required.force', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  resistance: () => Joi.object({
    resistance: uint()
      .when('$required.resistance', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  velocity: () => Joi.object({
    velocity: uint()
      .when('$required.velocity', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  stack: () => Joi.object({
    stack: uint()
      .min(1)
      .max(4096)
      .when('$required.stack', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  usable: () => Joi.object({
    usable: Joi.boolean()
      .when('$required.usable', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  embed_title: () => Joi.object({
    embed_title: Joi.string()
      .trim()
      .allow(null)
      .min(1)
      .max(96)
      .when('$required.embed_title', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  embed_description: () => Joi.object({
    embed_description: Joi.string()
      .trim()
      .allow(null)
      .min(1)
      .max(4096)
      .when('$required.embed_description', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  embed_url: () => Joi.object({
    embed_url: Joi.string()
      .trim()
      .allow(null)
      .uri()
      .when('$required.embed_url', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  appearance: () => Joi.object({
    appearance: Joi.string()
      .trim()
      .allow(null)
      .uri()
      .when('$required.appearance', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  banner: () => Joi.object({
    banner: Joi.string()
      .trim()
      .allow(null)
      .uri()
      .when('$required.banner', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  created_at: () => Joi.object({
    created_at: Joi.date()
      .when('$required.created_at', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  }),
  updated_at: () => Joi.object({
    updated_at: Joi.date()
      .when('$required.updated_at', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
  })
}

export default validate;