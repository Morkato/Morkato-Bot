import type { Role } from './role'

export type Guild = {
  id: string
  name: string
  icon: string
  icon_hash: string
  splash: string
  discovery_splash: string
  owner: boolean
  owner_id: string
  permissions: string
  region: string

  roles: Role[]

  [key: string]: any
}