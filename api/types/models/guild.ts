export type Guild = {
  id: string
}

export type GuildWhereParameter = {  }
export type GuildGetherParameter = Pick<Guild, 'id'>
export type GuildCreateParameter = { data: Pick<Guild, 'id'> }
export type GuildDeleteParameter = Pick<Guild, 'id'>

export type GuildWhereFunction = ({  }: GuildWhereParameter) => Promise<Guild[]>
export type GuildGetherFunction = ({ id }: GuildGetherParameter) => Promise<Guild>
export type GuildCreateFunction = ({ data }: GuildCreateParameter) => Promise<Guild>
export type GuildDeleteFunction = ({ id }: GuildDeleteParameter) => Promise<Guild>

export type GuildDatabase = {
  findGuild: GuildWhereFunction
  getGuild: GuildGetherFunction
  createGuild: GuildCreateFunction
  delGuild: GuildDeleteFunction
}

export type GuildNotifyType =
  | 'guild.create'
  | 'guild.delete'