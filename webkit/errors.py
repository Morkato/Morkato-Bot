from typing import Optional, Union, Dict, List, Tuple, Any

import aiohttp

def _flatten_error_dict(d: Dict[str, Any], key: str = '') -> Dict[str, str]:
  items: List[Tuple[str, str]] = []
  for k, v in d.items():
    new_key = key + '.' + k if key else k

    if isinstance(v, dict):
      try:
          _errors: List[Dict[str, Any]] = v['_errors']
      except KeyError:
        items.extend(_flatten_error_dict(v, new_key).items())
        
        return
      
      items.append((new_key, ' '.join(x.get('message', '') for x in _errors)))
    else:
      items.append((new_key, v))

  return dict(items)

class HTTPException(Exception):
  """
    Um erro genérico HTTP
  """
  def __init__(self, response: aiohttp.ClientResponse, message: Optional[Union[str, Dict[str, Any]]]):
    self.response = response
    self.status: int = response.status
    self.code: int
    self.text: str
    
    if isinstance(message, dict):
      self.code = message.get('code', 0)
      
      base = message.get('message', '')
      errors = message.get('errors')
      
      self._errors: Optional[Dict[str, Any]] = errors
      
      if errors:
        errors = _flatten_error_dict(errors)
        helpful = '\n'.join('In %s: %s' % t for t in errors.items())
        
        self.text = base + '\n' + helpful

      else:
        self.text = base

    else:
      self.text = message or ''
      self.code = 0

    fmt = '{0.status} {0.reason} (error code: {1})'

    if len(self.text):
      fmt += ': {2}'

    super().__init__(fmt.format(self.response, self.code, self.text))

class BadRequest(HTTPException):
  """
    Erro lançado caso o servidor não entenda a requisição do cliente.

    Status: 400
  """

  pass

class Unauthorized(HTTPException):
  """
    Erro lançado caso o cliente não seja autorizado ao servidor.

    Status: 401
  """

  pass

class Forbidden(HTTPException):
  """
    O cliente não tem direitos de acesso ao conteúdo portanto o servidor está rejeitando dar a resposta. Diferente do código 401, aqui a identidade do cliente é conhecida.

    Status: 403
  """

  pass

class NotFound(HTTPException):
  """
    O servidor não pode encontrar o recurso solicitado. Este código de resposta talvez seja o mais famoso devido à frequência com que acontece na web.

    Status: 404
  """

  pass

class MethodNotAllowed(HTTPException):
  """
    O método de solicitação é conhecido pelo servidor, mas foi desativado e não pode ser usado.

    Status: 405
  """

  pass

class TooManyRequests(HTTPException):
  """
    O usuário enviou muitas requisições num dado tempo ("limitação de frequência").

    Status: 429
  """

class InternalServerError(HTTPException):
  """
    O servidor encontrou uma situação com a qual não sabe lidar.

    Status: +500
  """