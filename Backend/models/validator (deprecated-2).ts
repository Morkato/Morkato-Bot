import { ValidationError } from 'errors'

import Joi from 'joi'

const keys = {
  name<T extends (string | null)>(original?: T) {
    const schema = Joi.string()
      .trim()
      .regex(/^[\D0-9].+$/)
      .min(1)
      .max(32)
      .when('$required.name', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
      .when('$allow.name', { is: null, then: Joi.allow(null) })

    if(original === undefined) {
      return schema;
    }

    return schema.default(original);
  },
  id<T extends (string | null)>(original?: T) {
    const schema = Joi.string()
      .trim()
      .regex(/^[0-9]+$/)
      .when('$required.id', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
    
    if(original === undefined) {
      return schema;
    }

    return schema.default(original);
  },
  embed_title<T extends (string | null)>(original?: T) {
    const schema = Joi.string()
      .trim()
      .min(1)
      .max(96)
      .regex(/^[\D0-9].+$/)
      .allow(null)
      .when('$required.embed_title', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })

    if(original === undefined) {
      return schema;
    }

    return schema.default(original);
  },

  embed_description<T extends (string | null)>(original?: T) {
    const schema = Joi.string()
      .trim()
      .min(1)
      .max(4096)
      .regex(/^[\D0-9].+$/)
      .allow(null)
      .when('$required.embed_description', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
    
    if(original === undefined) {
      return schema;
    }

    return schema.default(original);
  },
  embed_url<T extends (string | null)>(original?: T) {
    const schema = Joi.string()
      .trim()
      .regex(/^(https?:\/\/[\D0-9]+|cdn:\/[\D0-9]+)$/)
      .allow(null)
      .when('$required.embed_url', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
    
    if(original === undefined) {
      return schema;
    }

    return schema.default(original);
  },
  type(valid: string[], original?: string) {
    const schema = Joi.number()
      .integer()
      .valid(...valid)

    if(original === undefined) {
      return schema;
    }

    return schema.default(original);
  },

  role: <T extends (string | null)>(original?: T) => keys.id(original),
  roles(original?: string[]) {
    const schema = Joi.array()
      .items(
        Joi.string()
          .trim()
          .regex(/^[0-9]+$/)
      )
      .when('$required.roles', { is: 'required', then: Joi.required(), otherwise: Joi.optional() })
    
    if(original === undefined) {
      return schema;
    }

    return schema.default(original);
  },
  created_at: () => Joi.date().allow(Joi.string()),
  updated_at: () => keys.created_at()
}

type DefaultKeys = typeof keys
type SchemaKeys = keyof DefaultKeys

type KeysType = (Partial<{
  [K in SchemaKeys]: 'required' | 'optional'
}> | KeysType[]) | { [key: string]: KeysType }

export function createSchema<
  Keys extends SchemaKeys[]
>(
  rows_keys: Keys,
  { params }: {
    params: Partial<Record<Keys[number], Parameters<DefaultKeys[Keys[number]]>>>
  }
): Joi.ObjectSchema<Record<Keys[number], ReturnType<DefaultKeys[Keys[number]]>>> {
  return Joi.object(Object.fromEntries(rows_keys.map(key => ([key, (keys[key])(...(params[key]))]))))
}

export default function validate<
  T extends any,
  Keys extends SchemaKeys[] = []
>(
  obj: Record<string, unknown>,
  keys: Partial<Record<SchemaKeys, 'required' | 'optional'>> & Partial<Record<keyof AdicionalKeys, 'required' | 'optional'>>,
  options?: {
    params?: Partial<Record<Keys[number], Parameters<DefaultKeys[Keys[number]]>>>,
  }
): T {
  try {
    obj = JSON.parse(JSON.stringify(obj))
  } catch {
    throw new ValidationError({ message: "O body tem que ser um Json.", action: "Tente enviar um Json desssa vez." })
  }

  const schema = createSchema(Object.keys(keys) as Keys, { params: options?.params })

  const { error, value } = schema.validate(obj, {
    context: {
      required: keys
    }
  })

  if (!error)
    return value as T;

  throw new ValidationError({
    message: error.details[0].message,
    key: error.details[0].context.key || error.details[0].context.type || 'object',
    errorLocationCode: 'MODEL:VALIDATOR:SCHEMA',
    type: error.details[0].type
  });
}