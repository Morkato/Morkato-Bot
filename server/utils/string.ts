import unidecode from 'remove-accents'

export namespace string {
  export function format(text: string, params: Record<string, string>) {
    const regex = /(\$(?<key>\$|[^ \n\t]+))/g

    for (let { groups } of text.matchAll(regex)) {
      if (groups) {
        const key = groups.key

        text = text.replace(`$${key}`, params[key] || '')
      }
    }

    return text;
  }
}

type StringStripParams = {
  ignore_accents?: boolean
  ignore_empty?: boolean
  case_insensitive?: boolean
  trim?: boolean
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

export default string;