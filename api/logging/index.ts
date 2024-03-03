import type { Logger as ILogger } from 'type:logging'

import { LoggerLevel } from 'type:logging'
import { StringView } from './view'

const levelnames: Record<LoggerLevel, string> = {
  [LoggerLevel.DEBUG]: "DEBUG",
  [LoggerLevel.INFO]: "INFO",
  [LoggerLevel.WARNING]: "WARNING",
  [LoggerLevel.ERROR]: "ERROR",
  [LoggerLevel.CRITICAL]: "CRITICAL"
}

class Logger implements ILogger {
  static loggers: Record<string, Logger | undefined> = {  }
  
  static _getUniqueLogger(name: string): Logger {
    let logger = Logger.loggers[name]

    if (!logger) {
      logger = new Logger(name)
      Logger.loggers[name] = logger
    }

    return logger;
  }

  static getLogger(name: string): Logger {
    name = name.trim().replace(/\s/g, '')

    // @ts-ignore
    let logger: Logger = undefined
    const flags = name.split(/\./g)

    for (const flag of flags) {
      if (!logger) {
        logger = Logger._getUniqueLogger(flag)
        continue;
      }

      logger = logger.getSubLogger(flag)
    }

    return logger;
  }

  private readonly subLoggers: Partial<Record<string,  Logger>> = {}
  private currentLevel: LoggerLevel = LoggerLevel.INFO
  private currentFormatter: Partial<Record<LoggerLevel, string>> = {}
  private currentDateFormatter: Partial<Record<LoggerLevel, string>> = {}

  private readonly enabled: LoggerLevel[] = []

  getFullName(): string {
    if (this.subLogger) {
      return this.subLogger.getFullName() + '.' + this.name
    }

    return this.name;
  }
  getSubLogger(name: string): Logger {
    let logger = this.subLoggers[name]

    if (!logger) {
      logger = new Logger(name, this)
      this.subLoggers[name] = logger
    }

    return logger;
  }

  constructor(
    private readonly name: string,
    private readonly subLogger: Logger | undefined = undefined
  ) {  }

  setLevel(level: LoggerLevel): void {
    this.currentLevel = level
  }

  setFormatter(formatter: string): void {
    this.currentFormatter[this.currentLevel] = formatter
  }

  getFormatter(level?: LoggerLevel): string {
    if (this.subLogger && this.currentFormatter[level ?? this.currentLevel] === undefined) {
      return this.subLogger.getFormatter(level);
    }

    return this.currentFormatter[level ?? this.currentLevel] ?? "%message";
  }

  getDateFormatter(level?: LoggerLevel): string {
    level = level ?? this.currentLevel

    if (this.subLogger && this.currentDateFormatter[level] === undefined) {
      return this.subLogger.getDateFormatter(level);
    }

    return this.currentDateFormatter[level] ?? "%Y-%m-%d %H:%M:%S";
  }

  setDateFormatter(level: LoggerLevel, formatter: string): void {
    this.currentDateFormatter[level] = formatter
  }

  enable(level: LoggerLevel): void {
    if (this.enabled.includes(level)) {
      return;
    }

    this.enabled.push(level)
  }

  isEnabled(level: LoggerLevel): boolean {
    const enabled = this.enabled.includes(level)
    
    if (this.subLogger && !enabled) {
      return this.subLogger.isEnabled(level);
    }

    return enabled;
  }

  _log(level: LoggerLevel, message: string, error?: Error, ...args: string[]) {
    if (!this.isEnabled(level)) {
      return;
    }

    const date = StringView.timeFormat(new Date(Date.now()), this.getDateFormatter(level));
    const formatter = this.getFormatter(level)
    
    message = StringView.formatLoggerSintaxe(message, args, {})

    if ([LoggerLevel.DEBUG, LoggerLevel.INFO, LoggerLevel.WARNING].includes(level)) {
      message = StringView.formatLoggerSintaxe(formatter, [], {
        name: this.name,
        fullname: this.getFullName(),
        message, date,
        levelname: levelnames[level]
      })
    } else {
      message = StringView.formatLoggerSintaxe(formatter, [], {
        name: this.name,
        fullname: this.getFullName(),
        message, date,
        levelname: levelnames[level],
        errorname: error?.name ?? "Error",
        errormessage: error?.message,
        errorstack: error?.stack?.split(/\n/g).slice(1).join('\n')
      })
    }

    console.log(message)
  }

  debug(message: string, ...args: string[]) {
    this._log(LoggerLevel.DEBUG, message, undefined, ...args)
  }

  info(message: string, ...args: string[]) {
    this._log(LoggerLevel.INFO, message, undefined, ...args)
  }

  warn(message: string, ...args: string[]) {
    this._log(LoggerLevel.WARNING, message, undefined, ...args)
  }

  error(message: string, error: Error,  ...args: string[]) {
    this._log(LoggerLevel.ERROR, message, error, ...args)
  }

  critical(message: string, error: Error, ...args: string[]) {
    this._log(LoggerLevel.CRITICAL, message, error, ...args)
  }
}

// @ts-ignore
if (!global.morkato_logging_module) {
  // @ts-ignore
  global.morkato_logging_module = Logger.loggers
} else {
  // @ts-ignore
  Logger.loggers = global.morkato_logging_module
}

export function getLogger(name: string): ILogger {
  return Logger.getLogger(name);
}

export { LoggerLevel };