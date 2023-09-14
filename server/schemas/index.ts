import { ValidationError } from 'errors'

import Joi from 'joi'

function makeContext(schema: Joi.AnySchema, required: boolean) {
  if (required) {
    return schema.required();
  }

  return schema;
}

type AssertParams<T = any> = { obj: Record<string, unknown>, schema: Joi.ObjectSchema<T> }

type Props = {
  key:       string
  required?: boolean
}

type ObjectSchemaFunction = Record<string, (props: Props) => Joi.AnySchema> 

type SchemaPropsParams<
  ExtendSchema extends ObjectSchemaFunction = {}
> = Record<string, { key: keyof typeof schemas | keyof ExtendSchema, required?: boolean }>

export function getSchemaFromProps<ExtendParams extends ObjectSchemaFunction = {}>(props: SchemaPropsParams<ExtendParams>, extend?: ExtendParams) {
  extend = extend ?? {} as ExtendParams

  const allowed_schemas = Object.assign<typeof schemas, ExtendParams>(schemas, extend)

  const notResolvedSchema = Object.entries(props).map(([key, prop]) => {
    const callback = allowed_schemas[prop.key]

    return [key, callback({ key, required: prop.required })];
  })

  const schema = Joi.object(Object.fromEntries(notResolvedSchema)).required().min(1).messages({
    'object.base': `O Body deve ser do tipo "Json.Object"`,
    'object.min': `O Objeto enviado deve ter no mínimo 1 chave.`
  })

  return schema;
}

export function assert<T>({ obj, schema }: AssertParams<T>) {
  try {
    obj = JSON.parse(JSON.stringify(obj))
  } catch {
    throw new ValidationError({
      message: 'Não foi possível interpretar o valor enviado.',
      action: 'Verifique se o valor enviado é um JSON válido.',
      errorLocationCode: 'SCHEMA:VALIDATOR:ERROR_PARSING_JSON',
      key: 'obj'
    })
  }

  const { error, value } = schema.validate(obj)

  if(error) {
    throw new ValidationError({
      message: error.details[0].message,
      key: error.details[0]?.context?.key || error.details[0]?.context?.type || 'object',
      errorLocationCode: 'MODEL:VALIDATOR:SCHEMA',
      type: error.details[0].type
    });
  }

  return value;
}

export function validate<T, ExtendParams extends ObjectSchemaFunction = {}>(obj: Record<string, unknown>, props: SchemaPropsParams<ExtendParams>, extend?: ExtendParams) {
  const schema = getSchemaFromProps<ExtendParams>(props, extend)

  return assert<T>({ obj, schema });
}

const schemas = {
  id({ key, required = false }: Props) {
    const schema = Joi
      .string()
      .trim()
      .min(1)
      .regex(/^[0-9]+$/)
      .when('$.required.id', { is: true, then: Joi.required(), otherwise: Joi.optional() })
      .messages({
        'any.required': `O campo "${key}" é obrigatório.`,
        'string.empty': `O campo "${key}" não pode estar em branco.`,
        'string.base': `O campo "${key}" deve ser do tipo string.`,
        'string.regex': `O campo "${key}" deve seguir o regex: /^[0-9]+$/`
      });

    return makeContext(schema, required);
  },
  name({ key, required = false }: Props) {
    const schema = Joi
      .string()
      .trim()
      .min(1)
      .max(32)
      .regex(/^[^-+>@&$].+[^-+>@&$]$/)
      .messages({
        'any.required': `O campo "${key}" é obrigatório.`,
        'string.empty': `O campo "${key}" não pode estar em branco.`,
        'string.base': `O campo "${key}" deve ser do tipo string.`,
      });
    
    return makeContext(schema, required);
  },
  art_type({ key, required = false }: Props) {
    const schema = Joi
      .string()
      .trim()
      .valid('RESPIRATION', 'KEKKIJUTSU')

    return makeContext(schema, required);
  },
  player_breed({ key, required = false }: Props) {
    const schema = Joi
      .string()
      .trim()
      .valid('HUMAN', 'ONI', 'HYBRID')
    
    return makeContext(schema, required);
  },
  player_name({ key, required = false }: Props) {
    const schema = Joi
      .string()
      .trim()
      .valid('F', 'E', 'D', 'C', 'B', 'A', 'AA', 'AAA', 'AAAA', 'S', 'SS', 'SSS', 'SSSS')

    return makeContext(schema, required);
  },
  dialog_choose({ key, required = false }: Props) {
    const schema = Joi
      .string()
      .trim()
      .valid('PLAYER', 'NPC')

    return makeContext(schema, required);
  },
  embed_title({ key, required = false }: Props) {
    const schema = Joi
      .string()
      .trim()
      .allow(null)
      .min(1)
      .max(96)

    return makeContext(schema, required);
  },
  embed_description({ key, required = false }: Props) {
    const schema = Joi
      .string()
      .trim()
      .allow(null)
      .min(1)
      .max(4096)

    return makeContext(schema, required);
  },
  embed_url({ key, required = false }: Props) {
    const schema = Joi
      .string()
      .trim()
      .allow(null)
      .uri()

    return makeContext(schema, required);
  },
  created_at({ key, required = false }: Props) {
    const schema = Joi
      .date()
      .allow(Joi.string())

      return makeContext(schema, required);
  },
  updated_at({ key, required = false }: Props) {
    return schemas.created_at({ key, required });
  }
}