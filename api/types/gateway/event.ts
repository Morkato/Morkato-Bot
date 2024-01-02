export type PlayerEvent =
  | 'RAW_CREATE_PLAYER'
  | 'CREATE_PLAYER'
  | 'UPDATE_PLAYER'
  | 'DELETE_PLAYER'
  | 'RAW_PLAYER_INVENTORY'
  | 'INVENTORY_PLAYER_ITEM_ADD'
  | 'INVENTORY_PLAYER_ITEM_REMOVE'
  | 'INVENTORY_PLAYER_ITEM_UPDATE'

export type AttackEvent =
  | 'RAW_CREATE_ATTACK'
  | 'CREATE_ATTACK'
  | 'UPDATE_ATTACK'
  | 'DELETE_ATTACK'

export type GuildEvent =
  | 'RAW_CREATE_GUILD'
  | 'CREATE_GUILD'
  | 'DELETE_GUILD'

export type ItemEvent =
  | 'RAW_CREATE_ITEM'
  | 'CREATE_ITEM'
  | 'UPDATE_ITEM'
  | 'DELETE_ITEM'

export type ArtEvent =
  | 'RAW_CREATE_ART'
  | 'CREATE_ART'
  | 'UPDATE_ART'
  | 'DELETE_ART'

export type WebSocketEvent =
  | PlayerEvent
  | AttackEvent
  | GuildEvent
  | ItemEvent
  | ArtEvent