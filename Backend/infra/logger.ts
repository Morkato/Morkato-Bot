import { readFile, writeFile } from 'fs/promises'
import { existsSync, mkdirSync } from 'fs'
import { join } from 'path'

import stripColor from 'ansi-regex'
import AsyncLock from 'async-lock'
import chalk from 'chalk'

const cache: { lock: AsyncLock | null } = {
  lock: null
}

if(!process.env.BACKEND_LOG) {
  console.warn('BACKEND_LOG not set, enabling logging by default')

  process.env.BACKEND_LOG = 'on'
}

if(!process.env.REGISTRY_LOG) {
  console.warn('REGISTRY_LOG not set, enabling logging by default')

  process.env.REGISTRY_LOG = "on"
}

const dir = join(process.cwd(), '.logs')

if(!existsSync(dir) && process.env.REGISTRY_LOG === "on") {
  mkdirSync(dir)
}

interface LogSettings {
  appName?: string;
  functionName?: string;
  userName?: string;
  sessionId?: string;
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

export function info(message: string, {formated, registryLog, settings}: { formated?: string, registryLog?: boolean, settings?: LogSettings }): void {
  if(process.env.BACKEND_LOG !== "on")
    return;
  if(!formated)
    formated = `${chalk.bgBlackBright('info')} $date $app $user $func $session\n\t${chalk.blackBright('-')} $message`;
  const day = chalk.magenta(getNow())

  const prefixs = { date: day, message: chalk.blackBright(message), session: null, func: null, user: null }

  if(settings) {
    const { appName, functionName, userName, sessionId } = settings

    if(appName)
      prefixs['app'] = chalk.bgMagenta(`[App::${appName}]`);
    if(functionName)
      prefixs['func'] = chalk.greenBright(`[Func::${functionName}]`);
    if(userName)
      prefixs['user'] = `[User::${userName}]`;
    if(sessionId)
      prefixs['session'] = `[Session::${sessionId}]`
    
    for(let [ key, value ] of Object.entries(prefixs)) {
      formated = formated.replace(`$${key}`, value || '');
    }

    message = formated

    if(registryLog)
      registry(message, appName);
  }

  console.log(message)
}

export function warn(message: string, {formated, registryLog, settings}: { formated?: string, registryLog?: boolean, settings?: LogSettings }): void {
  if(process.env.BACKEND_LOG !== "on")
    return;
  if(!formated)
    formated = `${chalk.bgYellowBright('warn')} $date $app $user $func $session\n\t${chalk.yellowBright('-')} $message`;
  const day = chalk.magenta(getNow())

  const prefixs = { date: day, message: chalk.yellowBright(message), session: null, func: null, user: null }

  if(settings) {
    const { appName, functionName, userName, sessionId } = settings

    if(appName)
      prefixs['app'] = chalk.bgMagenta(`[App::${appName}]`);
    if(functionName)
      prefixs['func'] = chalk.greenBright(`[Func::${functionName}]`);
    if(userName)
      prefixs['user'] = `[User::${userName}]`;
    if(sessionId)
      prefixs['session'] = `[Session::${sessionId}]`

    for(let [ key, value ] of Object.entries(prefixs)) {
      formated = formated.replace(`$${key}`, value || '');
    }
  
    message = formated

    if(registryLog)
      registry(message, appName);
  }


  console.warn(message)
}

export function err(message: string, {formated, error, exit, registryLog, settings}: { formated?: string, error?: Error, exit?: boolean, registryLog?: boolean, settings?: LogSettings }): void {
  if(process.env.BACKEND_LOG !== "on") {
    if(exit) {
      throw error || new Error(message);
    }

    return;
  }

  if(!formated)
    formated = `${chalk.bgRed('error')} $date $app $user $func $session\n\t${chalk.redBright('-')} $message`;

  const day = chalk.magenta(getNow())

  const prefixs = { date: day, message: chalk.redBright(message), session: null, func: null, user: null }

  if(settings) {
    const { appName, functionName, userName, sessionId } = settings

    if(appName)
      prefixs['app'] = chalk.bgMagenta(`[App::${appName}]`);
    if(functionName)
      prefixs['func'] = chalk.greenBright(`[Func::${functionName}]`);
    if(userName)
      prefixs['user'] = `[User::${userName}]`;
    if(sessionId)
      prefixs['session'] = `[Session::${sessionId}]`

    for(let [ key, value ] of Object.entries(prefixs)) {
      formated = formated.replace(`$${key}`, value || '');
    }
    
    message = formated
    
    if(registryLog)
      registry(message, appName);
  }

  if (error) {
    message += `\n\n${chalk.gray(error.stack || error.message)}`
  }

  console.error(message)

  if(exit)
    process.exit(1);
}


export default function createLog(settings: { appName: string, format?: string, registryLog?: boolean, errorExit?: boolean}) {
  return {
    info: (message: string, { config, registryLog }: { config?: LogSettings, registryLog?: boolean }) => info(
      message, {
        registryLog: registryLog === undefined ? false : registryLog,
        formated: settings.format,
        settings: { ...config, ...settings }
      }),
    warn: (message: string, { config, registryLog }: { config?: LogSettings, registryLog?: boolean }) => warn(
      message, {
        registryLog: registryLog === undefined ? false : registryLog,
        formated: settings.format,
        settings: { ...config, ...settings }
      }),
    error: (message: string, {error, exit, registryLog, config}: { error?: Error, exit?: boolean, registryLog?: boolean, config?: LogSettings }) => err(
      message, {
        error: error,
        exit: exit === undefined ? (settings.errorExit || false) : exit,
        formated: settings.format,
        registryLog: registryLog === undefined ? false : registryLog,
        settings: { ...config, ...settings }
      })
  }
}