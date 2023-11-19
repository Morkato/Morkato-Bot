export type Permission =
  | 'MANAGE:GUILDS'
  | 'MANAGE:ARTS'
  | 'MANAGE:ATTACKS'
  | 'MANAGE:PLAYERS'
  | 'MANAGE:ITEMS'
  | 'MANAGE:PLAYER:ITEMS'

export type User = {
  name: string
  expire_at: number
  permissions: Permission[]
}
export const users: Record<string, User> = {
  anonymous: {
    name: 'anonymous',
    expire_at: -1,
    permissions: []
  },
  morkato: {
    name: 'Morkato Bot',
    expire_at: -1, // Infinite.
    permissions: [
      'MANAGE:GUILDS',
      'MANAGE:ARTS',
      'MANAGE:ATTACKS',
      'MANAGE:PLAYERS',
      'MANAGE:ITEMS',
      'MANAGE:PLAYER:ITEMS',
    ]
  }
}

export function hasPermission(usr: User, permission: Permission) {
  return usr.permissions.includes(permission)
}