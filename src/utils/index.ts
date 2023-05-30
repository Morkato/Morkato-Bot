import DiscordApi, { SettingsInit } from './discordApi'

import originalString from './string'
import originalObject from './object'

export type DynamicKeyValue<T> = { [key: string]: T | undefined }

export namespace utils {
  export import string = originalString;
  export import object = originalObject;
  
  export async function discord(auth: string, settings?: SettingsInit) {
    return DiscordApi(auth, settings);
  }
}

export default utils;