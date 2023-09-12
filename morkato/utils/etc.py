from typing import (
  Optional,
  Callable,
  Iterable,
  TypeVar,
  Generator,
  Union,

  overload,

  Any
)

from unidecode import unidecode
import discord
import re

class _UndefinedMissing:
  __slots__ = ()

  def __eq__(self, other) -> bool:
    return False

  def __bool__(self) -> bool:
    return False

  def __hash__(self) -> int:
    return 0

  def __repr__(self):
    return 'undefined'

T = TypeVar('T')

UNDEFINED: Any   = _UndefinedMissing()
GenericGen = Generator[T, Any, Any]

def find(iter: Iterable[T], check: Callable[[T], bool]) -> GenericGen[T]:
  return (item for item in iter if check(item))

a = next(find([1, 2], lambda a: a==1))


def get(iter: Iterable[T], check: Callable[[T], bool]) -> Union[T, None]:
  return next(find(iter, check), None)

def format_text(text: str, default: Optional[str] = None, /, **kwargs) -> str:
	default = default or ''
  
	def repl(match: re.Match) -> str:
		result = kwargs.get(match['key'], default)
                
		if not isinstance(result, str):
			return str(result)

		return result

	return re.sub(r'(?<!\\)\$(?P<key>[\w_]+)', repl, text, flags=re.IGNORECASE)

def is_empty_text(text: str) -> bool:
  return not text.strip()

def strip_text(
  text: str, *,
  ignore_accents:   bool = UNDEFINED,
  ignore_empty:     bool = UNDEFINED,
  case_insensitive: bool = UNDEFINED,
  strip_text:       bool = UNDEFINED
) -> str:
  if not (
      ignore_accents
      and ignore_empty
      and case_insensitive
      and strip_text
  ) or is_empty_text(text):
    return text
  
  if strip_text:
    text = text.strip()

  if ignore_accents:
     text = unidecode(text)

  if ignore_empty:
     text = re.sub(r'\s+', '', text)
  
  if case_insensitive:
     text = text.lower()

  return text

def is_undefined(item) -> bool:
  return isinstance(item, _UndefinedMissing)

def nis_undefined(item) -> bool:
   return not is_undefined(item)

@overload
def case_undefined(item: T) -> Union[T, None]: ...
@overload
def case_undefined(item: T | _UndefinedMissing, default: T) -> T: ...
def case_undefined(item: T | _UndefinedMissing, default: Union[T, None] = UNDEFINED) -> T:
  if is_undefined(item):
     return default or None
  
  return item