from typing import (
  Optional,
  Callable,
  Coroutine,
  Literal,
  Iterable,
  TypeVar,
  Generator,
  Union,

  overload,

  List,
  Any
)
from numerize.numerize import numerize as num_fmt
from discord.ext       import commands
from unidecode         import unidecode

import discord
import re

try:
  import orjson

  from_json = orjson.loads

except ModuleNotFoundError:
  import json

  from_json = json.loads

FlagChecker = Literal['author', 'guild', 'channel', 'message']

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

UINT_LIMIT = 4294967295
UNDEFINED: Any   = _UndefinedMissing()
GenericGen = Generator[T, Any, Any]
EmptyCoro = Coroutine[Any, Any, None]

def find(iter: Iterable[T], check: Callable[[T], bool]) -> GenericGen[T]:
  return (item for item in iter if check(item))

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
  strip_text:       bool = UNDEFINED,

  empty: str = UNDEFINED
) -> str:
  if is_empty_text(text):
    return text
  
  if strip_text:
    text = text.strip()

  if ignore_accents:
     text = unidecode(text)

  if ignore_empty:
     text = re.sub(r'\s+', case_undefined(empty, '-'), text)
  
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

def message_checker(ctx: commands.Context, flags: List[FlagChecker]):
  def check(message: discord.Message) -> bool:
    if 'author' in flags and not message.author.id == ctx.author.id:
      return False
    
    if 'guild' in flags and not message.guild.id == ctx.guild.id:
      return False
    
    if 'channel' in flags and not message.channel.id == ctx.channel.id:
      return False
    
    return True
  
  return check

def reaction_checker(ctx: commands.Context, message: discord.Message, flags: List[FlagChecker]):
  def check(reaction: discord.Reaction, user: discord.User) -> bool:
    if 'author' in flags and not user.id == ctx.author.id:
      print('a')
      return False
    
    if 'guild' in flags and reaction.message.guild and not reaction.message.guild.id == ctx.guild.id:
      print('b')
      return False
    
    if 'channel' in flags and not reaction.message.channel.id == ctx.channel.id:
      print('c')
      return False
    
    if 'message' in flags and not reaction.message.id == message.id:
      print('d')
      return False
    
    return True
  
  return check

def in_range(num: Union[int, float], r: tuple[Union[int, float], Union[int, float]]) -> bool:
  if not isinstance(num, (int, float)):
    raise TypeError("Numbers only.")
  
  if not len(r) == 2:
    raise TypeError("Just a ray with two dimensions")

  start, end = min(r), max(r)

  if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
    raise TypeError("Numbers only.")

  return num == start if start == end else num >= start and num <= end

def get_attack(guild: "Guild", message: discord.Message):
  fmt_content = strip_text(message.content, strip_text=True, ignore_accents=True, ignore_empty=True, case_insensitive=True)

  attacks = (attack for attack in guild.attacks if strip_text(attack.name, strip_text=True, ignore_accents=True, ignore_empty=True, case_insensitive=True) in fmt_content)

  return max(attacks, key=lambda atk: len(atk.name))

async def async_all(iter: Iterable[Coroutine[Any, Any, Any]]) -> None:
  for coro in iter:
    await coro
