import type { DynamicKeyValue } from '.'

export namespace string {
  export function format(text: string, params: DynamicKeyValue<string>) {
    const regex = /(\$(?<key>\$|[^ \n\t]+))/g
  
    for(let { groups } of text.matchAll(regex)) {
      const key = groups.key
  
      text = text.replace(`$${key}`, params[key]||'')
    }
  
    return text;
  }
}

export default string;