import { uuid } from 'morkato/utils/uuid'

export interface ErrorParams {
  message?: string
  action?: string
  statusCode?: number
  errorId?: string
  requestId?: string
  errorLocationCode?: string
  key?: string
  type?: string
  databaseErrorCode?: number
}

export class BaseError extends Error {
  action?: string
  statusCode?: number
  errorId?: string
  requestId?: string
  errorLocationCode?: string
  key?: string
  type?: string
  databaseErrorCode?: number

  constructor({
    message,
    action,
    statusCode,
    errorId,
    requestId,
    errorLocationCode,
    key,
    type,
    databaseErrorCode,
  }: ErrorParams) {
    super();
    this.name = this.constructor.name;
    this.message = message || "Base error";
    this.action = action;
    this.statusCode = statusCode || 500;
    this.errorId = errorId || uuid();
    this.requestId = requestId;
    this.errorLocationCode = errorLocationCode;
    this.key = key;
    this.type = type;
    this.databaseErrorCode = databaseErrorCode;
  }
}

export class InternalServerError extends BaseError {
  constructor({ message, action, requestId, errorId, statusCode, errorLocationCode }: ErrorParams) {
    super({
      message: message || 'Um erro interno não esperado aconteceu.',
      action: action || "Informe ao suporte o valor encontrado no campo 'error_id'.",
      statusCode: statusCode || 500,
      requestId: requestId,
      errorId: errorId,
      errorLocationCode: errorLocationCode,
    });
  }
}

export class NotFoundError extends BaseError {
  constructor({ message, action, requestId, errorId, errorLocationCode, key }: ErrorParams) {
    super({
      message: message || 'Não foi possível encontrar este recurso no sistema.',
      action: action || 'Verifique se o caminho (PATH) e o método (GET, POST, PUT, DELETE) estão corretos.',
      statusCode: 404,
      requestId: requestId,
      errorId: errorId,
      errorLocationCode: errorLocationCode,
      key: key,
    });
  }
}

export class AlreadyExistsError extends BaseError {
  constructor({ message, action, requestId, errorId, errorLocationCode, key }: ErrorParams) {
    super({
      message: message || 'Esse Objeto já exists.',
      action: action || 'Tente passar dados diferentes.',
      statusCode: 409,
      requestId: requestId,
      errorId: errorId,
      errorLocationCode: errorLocationCode,
      key: key,
    });
  }
}

export class ServiceError extends BaseError {
  constructor({ message, action, statusCode, errorLocationCode, databaseErrorCode }: ErrorParams) {
    super({
      message: message || 'Serviço indisponível no momento.',
      action: action || 'Verifique se o serviço está disponível.',
      statusCode: statusCode || 503,
      errorLocationCode: errorLocationCode,
      databaseErrorCode: databaseErrorCode,
    });
  }
}

export class ValidationError extends BaseError {
  constructor({ message, action, statusCode, errorLocationCode, key, type }: ErrorParams) {
    super({
      message: message || 'Um erro de validação ocorreu.',
      action: action || 'Ajuste os dados enviados e tente novamente.',
      statusCode: statusCode || 400,
      errorLocationCode: errorLocationCode,
      key: key,
      type: type,
    });
  }
}

export class UnauthorizedError extends BaseError {
  constructor({ message, action, requestId, errorLocationCode }: ErrorParams) {
    super({
      message: message || 'Usuário não autenticado.',
      action: action || 'Verifique se você está autenticado com uma sessão ativa e tente novamente.',
      requestId: requestId,
      statusCode: 401,
      errorLocationCode: errorLocationCode,
    });
  }
}

export class ForbiddenError extends BaseError {
  constructor({ message, action, requestId, errorLocationCode }: ErrorParams) {
    super({
      message: message || 'Você não possui permissão para executar esta ação.',
      action: action || 'Verifique se você possui permissão para executar esta ação.',
      requestId: requestId,
      statusCode: 403,
      errorLocationCode: errorLocationCode,
    });
  }
}

export class TooManyRequestsError extends BaseError {
  constructor({ message, action, errorLocationCode }: ErrorParams) {
    super({
      message: message || 'Você realizou muitas requisições recentemente.',
      action: action || 'Tente novamente mais tarde ou contate o suporte caso acredite que isso seja um erro.',
      statusCode: 429,
      errorLocationCode: errorLocationCode,
    });
  }
}

export class UnprocessableEntityError extends BaseError {
  constructor({ message, action, errorLocationCode }: ErrorParams) {
    super({
      message: message || 'Não foi possível realizar esta operação.',
      action: action || 'Os dados enviados estão corretos, porém não foi possível realizar esta operação.',
      statusCode: 422,
      errorLocationCode: errorLocationCode,
    });
  }
}

export default {}