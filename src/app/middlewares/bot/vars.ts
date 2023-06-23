import type { NextResult, NextRequest, CustomContext } from 'app/middlewares'
import type { Guild } from 'models/guild'

import Vars, { type Variable } from 'models/varialbles'

import { param } from 'app/middlewares/utils'
import { guild } from './guild'

import client from 'infra/database'

const vars = Vars(client.varialble)

export function variable(handle: (req: NextRequest, ctx: CustomContext, { guild, variable }: { guild: Guild, variable: Variable }) => NextResult) {
  return param(async (req, ctx, name) => {
    return await guild(async (req, ctx, guild) => {
      const variable = await vars.get({ guild, name })

      return await handle(req, ctx, { guild, variable });
    })(req, ctx)
  }, 'var_name')
}

export function variables(handle: (req: NextRequest, ctx: CustomContext, { guild, variables }: { guild: Guild, variables: Variable[] }) => NextResult) {
  return guild(async (req, ctx, guild) => {
    const variables = await vars.getAll({ guild })

    return await handle(req, ctx, { guild, variables });
  })
}

export function forCreateVariable(handle: (req: NextRequest, ctx: CustomContext, { guild, variable }: { guild: Guild, variable: Variable }) => NextResult) {
  return guild(async (req, ctx, guild) => {
    const variable = await vars.create({ guild, data: await req.json() })

    return await handle(req, ctx, { guild, variable })
  })
}

export function forEditVar(handle: (req: NextRequest, ctx: CustomContext, { guild, before, after }: { guild: Guild, before: Variable, after: Variable }) => NextResult) {
  return variable(async (req, ctx, { guild, variable }) => {
    const after = await vars.edit({ guild, variable, data: await req.json() })

    return await handle(req, ctx, { guild, before: variable, after });
  })
}

export function forDelVar(handle: (req: NextRequest, ctx: CustomContext, { guild, variable }: { guild: Guild, variable: Variable }) => NextResult) {
  return variable(async (req, ctx, { guild, variable }) => {
    const deletedVar = await vars.del({ guild, variable })

    return await handle(req, ctx, { guild, variable: deletedVar });
  })
}