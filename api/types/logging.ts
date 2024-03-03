export interface ModuleOrganization {
  [key: string]: ModuleOrganization
}

export enum LoggerLevel {
  DEBUG = 0,
  INFO = 1,
  WARNING = 2,
  ERROR = 3,
  CRITICAL = 4
}

export interface Logger {
  setLevel(level: LoggerLevel): void
  
  getFormatter(level: LoggerLevel): string
  setFormatter(formatter: string): void

  getDateFormatter(level: LoggerLevel): string
  setDateFormatter(level: LoggerLevel, formatter: string): void

  enable(level: LoggerLevel): void
  isEnabled(level: LoggerLevel): boolean
  
  debug(message: string, ...args: string[]): void
  info(message: string, ...args: string[]): void
  warn(message: string, ...args: string[]): void
  error(message: string, error?: Error,  ...args: string[]): void
  critical(message: string, error?: Error,  ...args: string[]): void
}

declare global {
  export const morkato_logging_module: Record<string, Logger | undefined>
}