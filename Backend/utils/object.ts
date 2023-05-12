import { DynamicKeyValue } from '.'

export namespace object {
  export function map<AfterValue = any, BeforeValue = any>(obj: DynamicKeyValue<AfterValue>, map: (props: [string, AfterValue]) => BeforeValue) {
    return Object.fromEntries(Object.entries(obj).map(([key, value]) => [ key, map([key, value]) ]));
  }
  export function filter<AfterValue = any, BeforeValue = any>(obj: DynamicKeyValue<AfterValue>, filter: (props: [string, AfterValue]) => boolean) {
    return Object.fromEntries(Object.entries(obj).filter(([key, value]) => filter([key, value])))
  }
}

export default object;