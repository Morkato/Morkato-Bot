export type RoleTags = {
  bot_id: string
  integration_id: string
  premium_subscriber: null
  subscription_listing_id: string
  available_for_purchase: null
  guild_connections: null
}

export type Role = {
  id: string
  name: string
  color: string
  hoist: boolean
  icon: string
  unicode_emoji: string
  position: number
  managed: string
  mentionable: boolean
  tags: RoleTags
}