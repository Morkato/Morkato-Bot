import { getLogger, LoggerLevel } from "logging"

const defaultLoggerDateFormatter = "[%date]"
const loggerDateFormatter: Partial<Record<LoggerLevel, string>> = {}

const defaultLevelnameFormatter = "[%levelname/%fullname]"
const loggerLevelnameFormatter: Partial<Record<LoggerLevel, string>> = {}

const defaultLoggerMessageFormatter = "%message"
const loggerMessageFormatter: Partial<Record<LoggerLevel, string>> = {}

export function setupLogging(enabledLevels: string) {
  const logger = getLogger("morkato")
  const levels: LoggerLevel[] = [
    LoggerLevel.DEBUG,
    LoggerLevel.INFO,
    LoggerLevel.WARNING,
    LoggerLevel.ERROR,
    LoggerLevel.CRITICAL
  ]

  for (let level of enabledLevels.split(',')) {
    level = level.replace(/\s/g, '')

    if (level === 'debug') {
      logger.enable(LoggerLevel.DEBUG)
    } else if (level === 'info') {
      logger.enable(LoggerLevel.INFO)
    } else if (level === 'warning') {
      logger.enable(LoggerLevel.WARNING)
    } else if (level === 'error') {
      logger.enable(LoggerLevel.ERROR)
    } else if (level === 'critical') {
      logger.enable(LoggerLevel.CRITICAL)
    }
  }

  for (const level of levels) {
    logger.setLevel(level)

    let finalFormatter = ""

    finalFormatter += loggerDateFormatter[level] ?? defaultLoggerDateFormatter
    finalFormatter += ' '
    finalFormatter += loggerLevelnameFormatter[level] ?? defaultLevelnameFormatter
    finalFormatter += ' '
    finalFormatter += loggerMessageFormatter[level] ?? defaultLoggerMessageFormatter
    finalFormatter += ' '

    logger.setFormatter(finalFormatter)
  }
}