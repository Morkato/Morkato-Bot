export { object } from './object'
export { string } from './string'

import unidecode from 'remove-accents'

export function toKey(text: string) {
  return unidecode(text).trim().toLowerCase().replaceAll(' ', '-');
}