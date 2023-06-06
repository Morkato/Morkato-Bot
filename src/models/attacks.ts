import type { PrismaClient } from "@prisma/client"

import { type Art, type ArtType, validateArt } from 'models/validator/art'
import { selectMembersInAttacksFields } from 'models/attacks_fields'
import { type Guild, validateGuild } from 'models/validator/guild'
import { type Attack, validateAttack } from "./validator/attack"

import { assertSchema, schemas } from "./validator/utils"

import unidecode from 'remove-accents'

export const selectMembersInAttacks = {
    name: true,

    roles: true,
    required_roles: true,
    required_exp: true,

    damage: true,
    stamina: true,

    embed_title: true,
    embed_description: true,
    embed_url: true,

    fields: { select: selectMembersInAttacksFields },

    created_at: true,
    updated_at: true
}

export function toKey(text: string) {
  return unidecode(text).trim().toLowerCase().replace(' ', '-');
}

export default function Attacks(prisma: PrismaClient['attack']) {
  async function getAttacks({ guild, art }: { guild: Guild, art: Art<ArtType> }): Promise<Attack[]> {
    validateGuild(guild)
    validateArt(art)

    const attacks = await prisma.findMany({ where: { guild_id: guild.id, art_key: toKey(art.name) }, select: selectMembersInAttacks  })

    return attacks;
  }
  async function getAttack({ guild, name }: { guild: Guild, name: string }): Promise<Attack> {
    assertSchema(schemas.name.required(), name)
    validateGuild(guild)

    const attack = await prisma.findUnique({ where: { key_guild_id: { key: toKey(name), guild_id: guild.id } }, select: selectMembersInAttacks })

    return attack;
  }
  async function createAttack({ guild, art, name }: { guild: Guild, art: Art<ArtType>, name: string }) {
    assertSchema(schemas.name.required(), name)
    validateGuild(guild)
    validateArt(art)

    const attack = await prisma.create({ data: { art_key: toKey(art.name), guild_id: guild.id, name, key: toKey(name) }, select: selectMembersInAttacks })

    art.attacks.push(attack)

    return attack;
  }
  async function editAttack({ guild, attack, data }: { guild: Guild, attack: Attack, data: Omit<Partial<Attack>, 'fields'> }): Promise<Attack> {
    validateAttack(attack)
    validateGuild(guild)

    const editedAttack = await prisma.update({ where: { key_guild_id: { key: toKey(attack.name), guild_id: guild.id } }, data, select: selectMembersInAttacks })

    return editedAttack;
  }
  async function delAttack({ guild, attack }: { guild: Guild, attack: Attack }): Promise<Attack> {
    validateAttack(attack)
    validateGuild(guild)

    const deletedAttack = await prisma.delete({ where: { key_guild_id: { key: toKey(attack.name), guild_id: guild.id } }, select: selectMembersInAttacks })

    return deletedAttack;
  }

  return { getAttacks, getAttack, createAttack, editAttack, delAttack };
}

export { Attacks, type Attack };