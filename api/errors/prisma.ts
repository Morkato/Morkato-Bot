import { NotFoundError, AlreadyExistsError, InternalServerError } from "."

export const anonymous = 'generic.unknown'

const pes = {
  P2002: {
    fkey: {
      guild_id: 'guild.alreadyexists',
      art_id: 'art.alreadyexists',
      item_id: 'item.alreadyexists',
      parent_id: 'attack.alreadyexists',
      player_id: 'player.alreadyexists'
    },
    key: {
      guild_id: 'guild.alreadyexists',
      art_id: 'art.alreadyexists',
      item_id: 'item.alreadyexists',
      parent_id: 'attack.alreadyexists',
      player_id: 'player.alreadyexists'
    }
  },
  P2003: {
    fkey: {
      guild_id: 'guild.notfound',
      art_id: 'art.notfound',
      item_id: 'item.notfound',
      parent_id: 'attack.notfound',
      player_id: 'player.notfound'
    }
  }
}

export function prismaError(err: any): string {
  try {
    const fields = (err.meta.field_name as string).split(' ', 1)[0].split(/\./g)
    const errors = (pes as any)[err.code] ?? anonymous
    let type = errors

    for (let field of fields) {
      type = type[field];
    }

    return type ?? anonymous;
  } catch {
    return anonymous;
  }
}

export const errors = {
  'generic.unknown': (name: string, location: string) => new InternalServerError({
    message: `O servidor encontrou uma situação na qual não sabe lidar. Nome: ${name}`,
    action: `Notifique ao meu desenvolvedor.`,
    errorLocationCode: location,
    type: 'generic.unknown'
  }),
  'guild.notfound': (id: string) => new NotFoundError({
    message: `O servidor (ID: ${id}) requer configuração.`,
    action: 'Tente configurá-lo antes.',
    type: 'guild.notfound'
  }),
  'art.notfound': (gid: string, id: string) => new NotFoundError({
    message: `A arte (ID: ${id}) não existe nessa guilda (ID: ${gid}).`,
    action: 'Tente novamente com um ID diferente, que seja correto.',
    type: 'art.notfound'
  }),
  'item.notfound': (gid: string, id: string) => new NotFoundError({
    message: `O item (ID: ${id}) não existe nessa guilda (ID: ${gid}).`,
    action: 'Tente novamente com um ID diferente, que seja correto.',
    type: 'item.notfound'
  }),
  'attack.notfound': (gid: string, id: string) => new NotFoundError({
    message: `O ataque (ID: ${id}) não existe nessa guilda (ID: ${gid}).`,
    action: 'Tente novamente com um ID diferente, que seja correto.',
    type: 'attack.notfound'
  }),
  'player.notfound': (gid: string, id: string) => new NotFoundError({
    message: `O player (ID: ${id}) não existe nessa guilda (ID: ${gid}).`,
    action: 'Tente novamente com um ID diferente, que seja correto.',
    type: 'player.notfound'
  }),
  'guild.alreadyexists': (id: string) => new AlreadyExistsError({
    message: `O servidor (ID: ${id}) já está configurado.`,
    action: 'Esse servidor já está configurado, tente editá-lo.',
    type: 'guild.alreadyexists'
  }),
  'art.alreadyexists': (gid: string, name: string) => new AlreadyExistsError({
    message: `A arte (Nome: ${name}) já existe nessa guilda (ID: ${gid}).`,
    action: 'Essa arte já existe, tente editá-la.',
    type: 'art.alreadyexists'
  }),
  'item.alreadyexists': (gid: string, name: string) => new AlreadyExistsError({
    message: `O item (Nome: ${name}) já existe nessa guilda (ID: ${gid}).`,
    action: 'Essa item já existe, tente editá-lo.',
    type: 'item.alreadyexists'
  }),
  'attack.alreadyexists': (gid: string, name: string) => new AlreadyExistsError({
    message: `O ataque (Nome: ${name}) já existe nessa guilda (ID: ${gid}).`,
    action: 'Essa ataque já existe, tente editá-lo.',
    type: 'attack.alreadyexists'
  }),
  'player.alreadyexists': (gid: string, name: string) => new AlreadyExistsError({
    message: `O player (Nome: ${name}) já existe nessa guilda (ID: ${gid}).`,
    action: 'Essa player já existe, tente editá-lo.',
    type: 'player.alreadyexists'
  }),
  'player-item.notfound': (gid: string, pid: string, iid: string) => new AlreadyExistsError({
    message: `Não existe o item: ${iid} no inventário do player: ${pid} da guilda: ${gid}`,
    action: 'Esse item não existe no inventário do player, tente criá-lo.',
    type: 'player-item.notfound'
  }),
  'player-item.alreadyexists': (gid: string, pid: string, iid: string) => new AlreadyExistsError({
    message: `O item: ${iid} já existe no inventário do player: ${pid} da guilda: ${gid}`,
    action: 'Essa item já existe já existe no inventário do player, tente editá-lo.',
    type: 'player-item.alreadyexists'
  })
}