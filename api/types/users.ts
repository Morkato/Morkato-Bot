export type Role =
  | 'MANAGE:GUILDS'
  | "MANAGE:PLAYERS"
  | "MANAGE:PLAYER:ITEMS"
  | "MANAGE:PLAYER:ARTS"
  | "MANAGE:ITEMS"
  | "MANAGE:ATTACKS"
  | "MANAGE:ARTS"

export type User = {
  name: string
  authorization: string
  roles: Role[]
}