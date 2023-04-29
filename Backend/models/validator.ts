import { ValidationError } from '@/erros'
import Joi, { AnySchema } from 'joi'

interface KeyOption {
  option: 0 | 1
  default?: string | number | boolean | null | (string | number | boolean | null)[]
  allow?: any[] | any
}

type ChoiceKeyOption = KeyOption | 0 | 1

export default function validator(obj: {
  [key: string]: string | number | boolean | null | (string | number | boolean | null)[]
}, keys: { [key: string]: ChoiceKeyOption }
): { [key: string]: string | number | boolean | null | (string | number | boolean | null)[] } {
  // Verifica se o "objeto" é um JSON valído.

  try {
    obj = JSON.parse(JSON.stringify(obj))
  } catch {
    throw new ValidationError({ message: "O body tem que ser um Json.", action: "Tente enviar um Json desssa vez." })
  }
  
  // Filtra as opções. Exemplo { 'required' = { option: 'required' } }.
  
  const filtereKeys = Object.fromEntries(Object.entries(keys).map(([key, val]) => [key, val === 0 || val === 1 ? { option: val } : val]))

  // Cria a Schema princípal.
  
  const schema = Joi.object(Object.fromEntries(
    Object.entries(filtereKeys).map(([key, value]) => [key, validators[key](value)])
  )).required().min(1)

  // Valida as informações
  
  const { error, value } = schema.validate(obj)

  if(error)
    throw new ValidationError({
      message: error.details[0].message,
      key: error.details[0].context.key || error.details[0].context.type || 'object',
      errorLocationCode: 'MODEL:VALIDATOR:SCHEMA',
      type: error.details[0].type
    });
  
  return value;
}

function createFlag<T extends any>(schema: AnySchema<T>) {
  return (option: KeyOption) => {
    if(option.allow !== undefined)
      schema = schema.allow(...(option.allow instanceof Array<any> ? option.allow : [option.allow,]));
    if(option.option === 1)
      schema = schema.required();
    else if(option.default !== undefined)
      schema = schema.default(option.default);
    
      
    return schema;
  }
}

const validators: { [key: string]: any } = {
  name: createFlag(Joi.string()
    .trim()
    .regex(/^[\D0-9].+$/)
    .min(2)
    .max(32)
  ),
  id: createFlag(Joi.string()
    .trim()
    .regex(/^[0-9]+$/)
  ),
  embed_title: createFlag(Joi.string()
    .allow(null)
    .trim()
    .regex(/^\D.+$/)
    .min(1)
    .max(96)
  ),
  embed_description: createFlag(Joi.string()
    .allow(null)
    .trim()
    .regex(/^\D.+$/)
    .min(1)
    .max(4096)
  ),
  embed_url: createFlag(Joi.string()
    .allow(null)
    .trim()
    .regex(/^((https?:\/\/)([\D0-9]+)|(\/[\D0-9]+))$/)
  ),
  guild_id: (option: KeyOption) => validators.id(option),
  role: (option: KeyOption) => validators.id(option)
}


/*
  * The number 0 means that an element will be optional, while the 1 means Required.
*/

const required = (): 1 => 1
const optional = (): 0 => 0

export { validator, required, optional }