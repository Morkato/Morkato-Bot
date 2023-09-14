import type { PlayerBreed, PlayerRank } from './player'

import { makeContext, assert } from './utils'
import { schemas }             from './utils'

import Joi from 'joi'

export type DialogChoose = 'PLAYER' | 'NPC'

export type DialogQuest = {
  id:       string
  guild_id: string
  quest_id: string

  position: number

  contents: string[]
  choose:   DialogChoose
}

export type Quest = {
  id:       string
  guild_id: string

  name: string

  required_breed:   PlayerBreed | null
  required_rank:    PlayerRank
  allowed_channels: string[]
  required_exp:     number

  title:       string | null
  description: string | null
  url:         string | null
  icon:        string | null

  dialogs: DialogQuest[]
}

const dialogQuestBaseSchema = {
  id:       schemas.id,
  guild_id: schemas.id,
  quest_id: schemas.id,

  position: Joi.number().integer(),

  contents: Joi.array().items(Joi.string().trim().min(1).max(2032)),
  choose:   Joi.string().valid('PLAYER', 'NPC')
}

const questBaseSchema = {
  id:       schemas.id,
  guild_id: schemas.id,

  name: schemas.name,

  required_breed:   schemas.player_breed,
  required_rank:    schemas.player_rank,
  allowed_channels: Joi.array().items(schemas.id),
  required_exp:     schemas.exp,

  title: schemas.embed_title,
  description: schemas.embed_description,
  url: schemas.embed_url,
  icon: schemas.embed_icon,
}

export function questSchema({ required, original }: {
  required: Partial<Record<keyof Quest, boolean> & { dialogs: Partial<Record<keyof DialogQuest, boolean>> }>
  original: Partial<Record<keyof Quest, any> & { dialogs: Partial<Record<keyof DialogQuest, any>> }>
}) {
  const required_dialogs = required.dialogs ?? {}
  const original_dialogs = original.dialogs ?? {}

  return Joi.object({
    id: makeContext(questBaseSchema.id, required['id'], original['id']),
    guild_id: makeContext(questBaseSchema.guild_id, required['guild_id'], original['guild_id']),

    name: makeContext(questBaseSchema.name, required['name'], original['name']),

    required_breed: makeContext(questBaseSchema.required_breed, required['required_breed'], original['required_breed']),
    required_rank: makeContext(questBaseSchema.required_rank, required['required_rank'], original['required_rank']),
    allowed_channels: makeContext(questBaseSchema.allowed_channels, required['allowed_channels'], original['allowed_channels']),
    required_exp: makeContext(questBaseSchema.required_exp, required['required_exp'], original['required_exp']),

    title: makeContext(questBaseSchema.title, required['title'], original['title']),
    description: makeContext(questBaseSchema.description, required['description'], original['description']),
    url: makeContext(questBaseSchema.url, required['url'], original['url']),
    icon: makeContext(questBaseSchema.icon, required['icon'], original['icon'])
  })   
}