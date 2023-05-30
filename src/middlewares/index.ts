import type { DynamicKeyValue } from 'utils'

import * as bot from './bot'

export type CustomContext = { params: DynamicKeyValue<string> }

export const middlewares = Object.freeze({
  bot: bot
})