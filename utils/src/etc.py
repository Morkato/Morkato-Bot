from typing import (
  Optional,
  TypeVar,
  Union,
  
  overload
)

from unidecode import unidecode

from decouple import config

import re

T = TypeVar('T')

@overload
def getEnv(key: str) -> Union[str, None]: ...
@overload
def getEnv(key: str, default: T) -> Union[str, T]: ...
def getEnv(key: str, default: Optional[T] = None) -> Union[str, None, T]:
  try:
    return str(config(key))
  except:
    return default

def format(text: str, default: Optional[str] = None, /, **kwargs) -> str:
	default = default or ''
  
	def repl(match: re.Match) -> str:
		result = kwargs.get(match['key'], default)
                
		if not isinstance(result, str):
			return str(result)

		return result

	return re.sub(r'(?<!\\)\$(?P<key>[\w_]+)', repl, text, flags=re.IGNORECASE)

def toKey(text: str) -> str:
  return unidecode(re.sub(r'\s+', '-', text.strip(), flags=re.IGNORECASE)).lower()