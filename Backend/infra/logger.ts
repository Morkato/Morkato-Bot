import { readFile, writeFile } from 'fs/promises'
import chalk, { ChalkInstance } from 'chalk'
import { existsSync, mkdirSync } from 'fs'
import { join } from 'path'

import stripColor from 'ansi-regex'
import AsyncLock from 'async-lock'

interface LogSettings {
  [key: string]: string
  functionName?: string
  userName?: string
  sessionId?: string
}

interface LogType<T extends string> {
  app: string
  forFormat: string
  registryLog?: boolean
  settings?: LogSettings
  type: T
}

interface LogInfo extends LogType<'infp'> {  }

const formatColorsLogTypes: { [key: string]: ChalkInstance } = {
  info: chalk.bgBlackBright
}

const cache: { lock: AsyncLock | null } = {
  lock: null
}

const dir = join(process.cwd(), '.logs')

if(!process.env.BACKEND_LOG) {
  console.warn('BACKEND_LOG not set, enabling logging by default')

  process.env.BACKEND_LOG = 'on'
}

if(!process.env.REGISTRY_LOG) {
  console.warn('REGISTRY_LOG not set, disabled logging by default')

  process.env.REGISTRY_LOG = "off"
}

if(!existsSync(dir) && process.env.REGISTRY_LOG === "on") {
  mkdirSync(dir)
}

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

async function registry(message: string, appName?: string) {
  if(process.env.REGISTRY_LOG !== "on")
    return;
  if(!cache.lock)
    cache.lock = new AsyncLock();
  
  appName = appName || ''
  const logPath = join(dir, `${appName}.log`)

  message = message.replace(stripColor(), '')

  await cache.lock.acquire(logPath, async () => {
    if(existsSync(logPath))
      message = `${(await readFile(logPath, { encoding: 'utf-8' })).toString()}\n\n${message}`;
    await writeFile(logPath, message, { encoding: 'utf-8' })
  })
}

function format(message: string, keys: { [key: string]: string }) {
  const formatter = /(\$(?<key>[^ \n\t]+))/g

  const keysOfText = message.matchAll(formatter)

  for(let { groups } of keysOfText)
    message = message.replace(`$${groups.key}`, keys[groups.key] || '');
  
    
  return message;
}

function log<T extends string>(message: string, { forFormat, app, registryLog, settings, type }: LogType<T>) {
  if(process.env.BACKEND_LOG !== "on")
    return;

  const method = 'info' ?  console.log : 'warn' ? console.warn : 'error' ? console.error : console.log
  const formatColor = formatColorsLogTypes[type] || chalk.bgBlueBright
  const formatedType = formatColor(type)
  const formatedApp = chalk.bgMagentaBright(`[App::${app}]`)
  const date = chalk.magenta(getNow())

  if(!settings) {
    const formatedMessage = format(forFormat, { type: formatedType, date: date, app: formatedApp, message: formatColor(message) })

    if(registryLog)
      registry(formatedMessage);

    method(formatedMessage)

    return;
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
  
  const formatedMessage = format(forFormat, { ...formatedSettings, type: formatedType, date: date, app: formatedApp, message })

  if(registryLog)
    registry(formatedMessage);
  
  method(formatedMessage)
}

export function info(message: string, { app, forFormat, registryLog, settings }: { app: string, forFormat: string, registryLog?: boolean, settings?: LogSettings }): void {
  return log(message, { type: 'info', app, forFormat, registryLog, settings });
}

export function warn(message: string, { app, forFormat, registryLog, settings }: { app: string, forFormat: string, registryLog?: boolean, settings?: LogSettings }): void {
  return log(message, { type: 'warn', app, forFormat, registryLog, settings });
}

export function err(message: string, { app, forFormat, registryLog, settings }: { app: string, forFormat: string, registryLog?: boolean, settings?: LogSettings }): void {
  return log(message, { type: 'error', app, forFormat, registryLog, settings });
}


export default ({ app, forFormat, registryLog }: { app: string, forFormat: string, registryLog?: boolean}) => ({
  info: (message: string, settings?: LogSettings) => info(message, { app, forFormat, registryLog, settings }),
  warn: (message: string, settings?: LogSettings) => warn(message, { app, forFormat, registryLog, settings }),
  error: (message: string, settings?: LogSettings) => err(message, { app, forFormat, registryLog, settings })
})