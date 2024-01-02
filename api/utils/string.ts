import unidecode from 'remove-accents'

const formatter = /((\\)?\$(?<key>\$|[^ \n\t.]+))/g

type StringStripParams = {
  ignore_accents?: boolean
  ignore_empty?: boolean
  case_insensitive?: boolean
  trim?: boolean
}


export function format(text: string, params: Record<string, string>) {
  return text.replace(formatter, sub => {
    if (sub[0] == '\\') {
      return sub.slice(1, sub.length);
    }

    sub = sub.slice(1, sub.length)
    
    return params[sub] ?? sub;
  })
}

export function is_empty(text: string): boolean {
  return !!text.match(/^\s*$/)
}

export function strip(text: string, {
  ignore_accents = false,
  ignore_empty = false,
  case_insensitive = false,
  trim = false
}: StringStripParams) {
  if (is_empty(text)) return text;

  if (trim) text = text.trim();
  if (ignore_accents) text = unidecode(text);
  if (case_insensitive) text = text.toLocaleLowerCase();
  if (ignore_empty) text = text.replace(/\s+/g, '-');

  return text;
}

export function stripAll(text: string): string {
  return strip(text, {
    ignore_accents: true,
    ignore_empty: true,
    case_insensitive: true,
    trim: true
  })
}

export default Object.freeze({ format, is_empty, strip, stripAll });