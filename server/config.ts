export type Permission = 
  | 'CREATE:GUILD'
  | 'CREATE:ART'
  | 'CREATE:ATTACK'
  | 'CREATE:PLAYER'
  | 'EDIT:GUILD'
  | 'EDIT:ART'
  | 'EDIT:ATTACK'
  | 'EDIT:PLAYER'
  | 'DELETE:GUILD'
  | 'DELETE:ART'
  | 'DELETE:ATTACK'
  | 'DELETE:PLAYER'


export type User = {
  login: string
  permissions: Permission[]
}
export const users: Record<string, User> = {
  Anonymous: {
    login: 'anonymous',
    permissions: []
  },
  MorkatoBot: {
    login: '...{more 64}',
    permissions: [
      'CREATE:GUILD',
      'CREATE:ART',
      'CREATE:ATTACK',
      'CREATE:PLAYER',
      'EDIT:GUILD',
      'EDIT:ART',
      'EDIT:ATTACK',
      'EDIT:PLAYER',
      'DELETE:GUILD',
      'DELETE:ART',
      'DELETE:ATTACK',
      'DELETE:PLAYER'
    ]
  }
}