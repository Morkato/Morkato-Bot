export type User = {
  username: string
  id: string
  discriminator: string
  avatar: string
  bot: boolean
  system: boolean
  flag: number

  [key: string]: any
}