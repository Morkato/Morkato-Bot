export namespace object {
  export function map<AfterValue = any, BeforeValue = any>(obj: Record<string, AfterValue>, map: (props: [string, AfterValue]) => BeforeValue) {
    return Object.fromEntries(Object.entries(obj).map(([key, value]) => [ key, map([key, value]) ]));
  }
  export function filter<AfterValue = any>(obj: Record<string, AfterValue>, filter: (props: [string, AfterValue]) => boolean) {
    return Object.fromEntries(Object.entries(obj).filter(([key, value]) => filter([key, value])))
  }
  export function exclude<TBefore, Keys extends keyof TBefore>(obj: TBefore, keys: Array<Keys>): Omit<TBefore, Keys> {
    return Object.fromEntries(Object.entries(obj).filter(([key, value]) => !keys.includes(key as Keys)))
  }
}

export default object;

export const {
  map,
  filter,
  exclude
} = object

const a = exclude({
  a: 1,
  b: 2
}, [ 'a' ])