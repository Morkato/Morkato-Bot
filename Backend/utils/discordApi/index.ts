import type { Guild } from './guild'
import type { User } from './user'
import type { Role } from './role'

import fetch, { RequestInit, Response, Headers } from 'node-fetch'

import {
  InternalServerError,
  NotFoundError
} from 'errors'

export type {
  Guild,
  User,
  Role
}

export type SettingsInit = {
  urls: {
    discord: {
      base: string
      api: string
      cdn: string
    }
  }
}

export type  DiscordConstructor = {
  (path: string, init?: RequestInit): Promise<Response>

  me(): Promise<User>
  user(id: string): Promise<Response>
  guild(id: string): Promise<Guild>
  guilds(): Promise<Guild[]>
}

export function DiscordApi(authorization: string, settings?: SettingsInit): DiscordConstructor {
  if(!settings)
    settings = {
      urls: {
        discord: {
          base: 'https://discord.com',
          api: 'https://discord.com/api/v9',
          cdn: 'https://cdn.discordapp.com'
        }
      }
    }

  const {
    base,
    api,
    cdn
  } = settings.urls.discord
  
  async function request(path: string, init?: RequestInit): Promise<Response> {
    if(!init) {
      const headers = new Headers()

      headers.set('authorization', authorization)

      return await fetch(`${api}${path}`, { headers: headers });
    }

    const headers = init.headers ? new Headers(init.headers) : new Headers()

    headers.set('authorization', authorization)

    return await fetch(`${api}${path}`, init);
  }
  
  return Object.assign(request, {
    async me(): Promise<User> {
      const res = await request('/users/@me')

      if(res.status !== 200) {
        throw new InternalServerError({
          message: '500: Um erro interno no servidor.',
          action: 'Parece ser um erro de autorização no discord, verifique se o token é valido.',
          statusCode: 500
        });
      }

      return await res.json()
    },
    async user(id: string) {
      return await request('/users/' + id);
    },
    async guild(id: string) {
      const response = await request(`/guilds/${id}`);
      
      if(response.status !== 200)
        throw new NotFoundError({ message: '404: O usuário não se encontra no servidor.', action: 'Tente novamente com um servidor valído ou verifique se o useário tá no tal servidor.', statusCode: 404 });
      
      return await response.json()
    },
    async guilds() {
      const response = await request('/users/@me/guilds');

      if(response.status !== 200)
        throw new InternalServerError({
          message: "500: Erro interno no servidor.",
          action: "Denuncie esse erro ao desenvolvedores, forneça a rota e a hora que foi feita a requisição.",
          statusCode: 500
        });
      
      return await response.json()
    }
  })
}

export default DiscordApi;