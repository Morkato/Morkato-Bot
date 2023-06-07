import type { PrismaClient } from "@prisma/client"

import valid, { type AttackField, validateAttackField } from "./validator/attack_field"

import { type Attack, validateAttack } from "./validator/attack"
import { type Guild, validateGuild } from './validator/guild'


import { assertSchema, schemas } from "./validator/utils"
import { toKey } from 'utils'

export const selectMembersInAttacksFields = {
  id: true,
  
  text: true,
  roles: true,

  created_at: true,
  updated_at: true
}

export default function attacksFields(prisma: PrismaClient['attackField']) {
  async function getFields({ guild, attack }: { guild: Guild, attack: Attack }): Promise<AttackField[]> {
    validateGuild(guild)
    validateAttack(attack)

    const fields = await prisma.findMany({ where: { guild_id: guild.id, attack_key: toKey(attack.name) }, select: selectMembersInAttacksFields })

    return fields;
  }
  async function getField({ guild, id }: { guild: Guild, id: string }): Promise<AttackField> {
    assertSchema(schemas.uuid.required(), id)
    validateGuild(guild)

    const field = await prisma.findUnique({ where: { guild_id_id: { guild_id: guild.id, id } }, select: selectMembersInAttacksFields })

    return field;
  }
  async function createField({ guild, attack, data }: { guild: Guild, attack: Attack, data: Omit<AttackField, 'id' | 'created_at' | 'updated_at'> }): Promise<AttackField> {
    validateGuild(guild)
    validateAttack(attack)

    data = valid<{ text: string, roles: string[] }>(data, { required: { text: true } })

    const field = await prisma.create({ data: { guild_id: guild.id, attack_key: toKey(attack.name), text: data.text, roles: data.roles }, select: selectMembersInAttacksFields })

    return field;
  }
  async function editField({ guild, field, data }: { guild: Guild, field: AttackField, data: Partial<Omit<AttackField, 'id' | 'created_at' | 'updated_at'>> }): Promise<AttackField> {
    validateGuild(guild)
    validateAttackField(field)

    const editedField = await prisma.update({ where: { guild_id_id: { guild_id: guild.id, id: field.id } }, data, select: selectMembersInAttacksFields })

    return editedField;
  }
  async function delField({ guild, field }: { guild: Guild, field: AttackField }): Promise<AttackField> {
    validateGuild(guild)
    validateAttackField(field)

    console.log(field)
    const deletedField = await prisma.delete({ where: { guild_id_id: { guild_id: guild.id, id: field.id } }, select: selectMembersInAttacksFields })
    console.log('aqui')

    return deletedField;
  }

  return { getField, getFields, createField, editField, delField }
}

export { type AttackField };