import type { NextResult, NextRequest, CustomContext } from 'middlewares'
import type { Art, ArtType } from 'models/validator/art'
import type { Guild } from 'models/validator/guild'

import { param } from 'middlewares/utils'
import { guild } from './guild'
import { art } from './art'

import Attacks, { Attack } from 'models/attacks'

import client from 'infra/database'

const attacks = Attacks(client.attack)

export function attack(handle: (req: NextRequest, ctx: CustomContext, { guild, attack }: { guild: Guild, attack: Attack }) => NextResult) {
  return param(async (req, ctx, name) => {
    return await guild(async (req, ctx, guild) => {
      const attack = await attacks.getAttack({ guild, name })

      return await handle(req, ctx, { guild, attack });
    })(req, ctx)
  }, 'attack_name')
}

export function forCreateAttack(handle: (req: NextRequest, ctx: CustomContext, { guild, art, attack }: { guild: Guild, art: Art<ArtType>, attack: Attack }) => NextResult) {
  return art(async (req, ctx, { guild, art }) => {
    const attack = await attacks.createAttack({ guild, art, name: (await req.json())?.name })

    return await handle(req, ctx, { guild, art, attack });
  })
}

export function forEditAttack(handle: (req: NextRequest, ctx: CustomContext, { guild, attack }: { guild: Guild, attack: Attack }) => NextResult) {
  return attack(async (req, ctx, { attack, guild }) => {
    const editedAttack = await attacks.editAttack({ guild, attack, data: await req.json() })

    return handle(req, ctx, { guild, attack: editedAttack });
  })
}

export function forDelAttack(handle: (req: NextRequest, ctx: CustomContext, { guild, attack }: { guild: Guild, attack: Attack }) => NextResult) {
  return attack(async (req, ctx, { guild, attack }) => {
    const deletedAttack = await attacks.delAttack({ guild, attack })

    return await handle(req, ctx, { guild, attack: deletedAttack });
  })
}