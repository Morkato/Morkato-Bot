import { readFile, writeFile } from 'fs/promises'
import { existsSync, mkdirSync } from 'fs'
import { join } from 'path'

import chalk, { ChalkInstance } from 'chalk'

import stripColor from 'ansi-regex'
import AsyncLock from 'async-lock'

export namespace global {
  export const logger = {
    LOG: true,
    REGISTRY: false
  }
}

export interface LogSettings {
  [key: string]: string
  functionName?: string
  userName?: string
  sessionId?: string
}

export interface LogType<T extends string> {
  app: string
  forFormat: string
  registryLog?: boolean
  settings?: LogSettings
  type: T
}

const formatColorsLogTypes: { [key: string]: ChalkInstance } = {
  info: chalk.greenBright,
  warn: chalk.yellowBright,
  error: chalk.redBright
}

const cache: { lock: AsyncLock | null } = {
  lock: null
}

const dir = join(process.cwd(), '.logs')

const getNow = () => {
  const now = (new Date())

  const day = '[ ' + now.toLocaleString('pt-BR', {
    year: '2-digit',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: 'numeric',
    second: 'numeric'
  }) + ' ]'

  return day;
}

export async function registry(message: string, app: string) {
  if(process.env.REGISTRY_LOG !== "on")
    return;
  if(!cache.lock)
    cache.lock = new AsyncLock();
  
  const logPath = join(dir, `${app}.log`)

  message = message.replace(stripColor(), '')

  await cache.lock.acquire(logPath, async () => {
    if(existsSync(logPath))
      message = `${(await readFile(logPath, { encoding: 'utf-8' })).toString()}\n\n${message}`;
    await writeFile(logPath, message, { encoding: 'utf-8' })
  })
}

export function format(message: string, keys: { [key: string]: string }) {
  const formatter = /(\$(?<key>[^ \n\t]+))/g

  const keysOfText = message.matchAll(formatter)

  for(let { groups } of keysOfText)
    message = message.replace(`$${groups.key}`, keys[groups.key] || '');
  
    
  return message;
}

function getLogFormatered<T extends string>(message: string, { forFormat, app, registryLog, settings, type }: LogType<T>) {
  const formatColor = formatColorsLogTypes[type] || chalk.bgBlueBright
  const formatedType = formatColor(type)
  const formatedApp = chalk.bgMagentaBright(`[App::${app}]`)
  const date = chalk.magenta(getNow())

  if(!settings) {
    const formatedMessage = format(forFormat, { type: formatedType, date: date, app: formatedApp, message: formatColor(message) })

    if(registryLog)
      registry(formatedMessage, app);

    return formatedMessage;
  }

  const { functionName, userName, sessionId, ...adicionalSettings } = settings

  const formatedSettings: { [key: string]: string } = {  }

  if(functionName)
    formatedSettings['func'] = chalk.greenBright(`[Func::${functionName}]`);
  if(userName)
    formatedSettings['user'] = chalk.whiteBright(`[User::${userName}]`);
  if(sessionId)
    formatedSettings['session'] = chalk.whiteBright(`[Session::${sessionId}]`);
  
  for(let [ key, value ] of Object.entries(adicionalSettings))
    formatedSettings[key] = chalk.blueBright(`[${key}::${value}]`);
  
  const formatedMessage = format(forFormat, { ...formatedSettings, type: formatedType, date: date, app: formatedApp, message: formatColor(message) })

  if(registryLog)
    registry(formatedMessage, app);
  
  return formatedMessage;
}

export function info(message: string, { app, forFormat, registryLog, settings }: { app: string, forFormat: string, registryLog?: boolean, settings?: LogSettings }): void {
  if(global.logger.LOG)
    return console.log(getLogFormatered(message, { type: 'info', app, forFormat, registryLog, settings }));

  return;
}

export function warn(message: string, { app, forFormat, registryLog, settings }: { app: string, forFormat: string, registryLog?: boolean, settings?: LogSettings }): void {
  if(global.logger.LOG)
    return console.warn(getLogFormatered(message, { type: 'warn', app, forFormat, registryLog, settings }));

  return;
}

export function err(message: string, { app, error, forFormat, registryLog, settings }: { app: string, error?: Error, forFormat: string, registryLog?: boolean, settings?: LogSettings }): void {
  if(global.logger.LOG)
    return console.error(getLogFormatered(message, { type: 'error', app, forFormat, registryLog, settings }));

  return;
}


export default function Logger({ app, forFormat, registryLog }: { app: string, forFormat: string, registryLog?: boolean}) {
  let printable = true

  if(!process.env.BACKEND_LOG) {
    console.warn('BACKEND_LOG not set, enabling logging by default')
  
    process.env.BACKEND_LOG = 'on'
  }
  
  if(!process.env.REGISTRY_LOG) {
    console.warn('REGISTRY_LOG not set, disabled logging by default')
  
    process.env.REGISTRY_LOG = "off"
  }
  
  if(process.env.REGISTRY_LOG === "on" && !existsSync(dir)) {
    mkdirSync(dir)
  }

  global.logger.LOG = process.env.BACKEND_LOG === 'on'
  global.logger.REGISTRY = process.env.REGISTRY_LOG === 'on' && (registryLog ?? false)
  
  return {
    info: (message: string, settings?: LogSettings) => printable ? info(message, { app, forFormat, registryLog: global.logger.REGISTRY, settings }) : null,
    warn: (message: string, settings?: LogSettings) => printable ? warn(message, { app, forFormat, registryLog: global.logger.REGISTRY, settings }) : null,
    error: (message: string, { settings, error }: { settings?: LogSettings, error?: Error }) => printable ? err(message, { app, error, forFormat, registryLog: global.logger.REGISTRY, settings }) : null,
    setPrintable: (set: boolean) => printable = set,
    setThisRegistryLog: (set: boolean) => {
      registryLog = set

      global.logger.REGISTRY = process.env.REGISTRY_LOG === 'on' && (registryLog ?? false)
    },
    setRegistryLogEnv: (set: 'on' | 'off') => {
      process.env.REGISTRY_LOG = set

      global.logger.REGISTRY = process.env.REGISTRY_LOG === 'on' && (registryLog ?? false)
    }
  };
}

export { Logger };