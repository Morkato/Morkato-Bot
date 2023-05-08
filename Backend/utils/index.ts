export type DynamicKeyValue<T> = { [key: string]: T | undefined }

export namespace utils {
  export namespace object {
    export function map<AfterValue = any, BeforeValue = any>(obj: DynamicKeyValue<AfterValue>, map: (props: [string, AfterValue]) => BeforeValue) {
      return Object.fromEntries(Object.entries(obj).map(([key, value]) => [ key, map([key, value]) ]));
    }
  }
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
}

export default utils;