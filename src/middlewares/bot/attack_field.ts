import type { NextResult, NextRequest, CustomContext } from 'middlewares'
import type { Attack } from 'models/attacks'
import type { Guild } from 'models/guild'

import AttacksFields, { type AttackField } from 'models/attacks_fields'

import { attack } from 'middlewares/bot/attack'
import { param } from 'middlewares'
import { guild } from './guild'

import client from 'infra/database'

const attacks_fields = AttacksFields(client.attackField)
const attackField_key = 'attackFieldId'

export function attacksFields(handle: (req: NextRequest, ctx: CustomContext, { guild, attack, fields }: { guild: Guild, attack: Attack, fields: AttackField[] }) => NextResult) {
  return attack(async (req, ctx, { guild, attack }) => {
    const fields = await attacks_fields.getFields({ guild, attack })

    return await handle(req, ctx, { guild, attack, fields });
  })
}

export function attackField(handle: (req: NextRequest, ctx: CustomContext, { guild, field }: { guild: Guild, field: AttackField }) => NextResult) {
  return param(async (req, ctx, id) => {
    return await guild(async (req, ctx, guild) => {
      const field = await attacks_fields.getField({ guild, id })

      return await handle(req, ctx, { guild, field });
    })(req, ctx)
  }, attackField_key)
}

export function forCreateAttackField(handle: (req: NextRequest, ctx: CustomContext, { guild, attack, field }: { guild: Guild, attack: Attack, field: AttackField }) => NextResult) {
  return attack(async (req, ctx, { guild, attack }) => {
    console.log('aqui')
    const field = await attacks_fields.createField({ guild, attack, data: await req.json() })

    return await handle(req, ctx, { guild, attack, field });
  })
}

export function forEditAttackField(handle: (req: NextRequest, ctx: CustomContext, { guild, beforeField, afterField }: { guild: Guild, beforeField: AttackField, afterField: AttackField }) => NextResult) {
  return attackField(async (req, ctx, { guild, field }) => {
    const editedField = await attacks_fields.editField({ guild, field, data: await req.json() })

    return await handle(req, ctx, { guild, beforeField: field, afterField: editedField });
  })
}

export function forDelAttackField(handle: (req: NextRequest, ctx: CustomContext, { guild, field }: { guild: Guild, field: AttackField }) => NextResult) {
  return attackField(async (req, ctx, { guild, field }) => {
    const deletedField = await attacks_fields.delField({ guild, field })

    return await handle(req, ctx, { guild, field: deletedField });
  })
}