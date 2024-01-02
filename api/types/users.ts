export type Role =
  | 'MANAGE:GUILDS'
  | "MANAGE:PLAYERS"
  | "MANAGE:PLAYER:ITEMS"
  | "MANAGE:ITEMS"
  | "MANAGE:ATTACKS"
  | "MANAGE:ARTS"

export type User = {
  name: string
  authorization: string
  roles: Role[]
}