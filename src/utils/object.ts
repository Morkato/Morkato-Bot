export namespace object {
  export function map<AfterValue = any, BeforeValue = any>(obj: Record<string, AfterValue>, map: (props: [string, AfterValue]) => BeforeValue) {
    return Object.fromEntries(Object.entries(obj).map(([key, value]) => [ key, map([key, value]) ]));
  }
  export function filter<AfterValue = any>(obj: Record<string, AfterValue>, filter: (props: [string, AfterValue]) => boolean) {
    return Object.fromEntries(Object.entries(obj).filter(([key, value]) => filter([key, value])))
  }
}

export default object;