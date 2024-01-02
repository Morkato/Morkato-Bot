from __future__ import annotations

from typing import (
	TYPE_CHECKING,
	Optional,
	Generator,
	Iterable,
	Callable,
	Sequence,
	TypeVar,
  Literal,
	Collection,
	Union,
	List,
	SupportsIndex,
	Any,
	Iterator,
	overload
)

if TYPE_CHECKING:
	from morkato.context import MorkatoContext
  
	from discord.reaction import Reaction
	from discord.message import Message
	from discord.user import User
     
	from ..attack import Attack
	from ..abc import Snowflake

from numerize.numerize import numerize as num_fmt
from functools import cached_property
from datetime import datetime
from unidecode import unidecode

import re

FlagChecker = Literal['author', 'guild', 'channel', 'message']
T_co = TypeVar('T_co', covariant=True)
T = TypeVar('T')
R = TypeVar('R')

MORKATO_EPOCH = 1672531200000
MORKATO_SNOWFLAKE_BITS = 8
MORKATO_SNOWFLAKE_SEQ = 24

def message_checker(ctx: MorkatoContext, flags: List[FlagChecker]):
  def check(message: Message) -> bool:
    if 'author' in flags and not message.author.id == ctx.author.id:
      return False
    
    if 'guild' in flags and not message.guild.id == ctx.guild.id:
      return False
    
    if 'channel' in flags and not message.channel.id == ctx.channel.id:
      return False
    
    return True
  
  return check

def reaction_checker(ctx: MorkatoContext, message: Message, flags: List[FlagChecker]):
  def check(reaction: Reaction, user: User) -> bool:
    if 'author' in flags and not user.id == ctx.author.id:
      return False
    
    if 'guild' in flags and reaction.message.guild and not reaction.message.guild.id == ctx.guild.id:
      return False
    
    if 'channel' in flags and not reaction.message.channel.id == ctx.channel.id:
      return False
    
    if 'message' in flags and not reaction.message.id == message.id:
      return False
    
    return True
  
  return check

class SequenceProxy(Sequence[T_co]):
	def __init__(self, proxied: Collection[T_co], *, sorted: Optional[Callable[[T_co], int]] = None):
		self.__proxied: Collection[T_co] = proxied
		self.__sorted = sorted

	@cached_property
	def __copied(self) -> List[T_co]:
		if self.__sorted is not None:
			self.__proxied = sorted(self.__proxied, key=self.__sorted)
		else:
			self.__proxied = list(self.__proxied)
		return self.__proxied

	def __repr__(self) -> str:
		return f"SequenceProxy({self.__proxied!r})"

	@overload
	def __getitem__(self, idx: SupportsIndex) -> T_co:
		...

	@overload
	def __getitem__(self, idx: slice) -> List[T_co]: ...

	def __getitem__(self, idx: Union[SupportsIndex, slice]) -> Union[T_co, List[T_co]]:
		return self.__copied[idx]

	def __len__(self) -> int:
		return len(self.__proxied)

	def __contains__(self, item: Any) -> bool:
		return item in self.__copied

	def __iter__(self) -> Iterator[T_co]:
		return iter(self.__copied)

	def __reversed__(self) -> Iterator[T_co]:
		return reversed(self.__copied)

	def index(self, value: Any, *args: Any, **kwargs: Any) -> int:
		return self.__copied.index(value, *args, **kwargs)

	def count(self, value: Any) -> int:
		return self.__copied.count(value)

def format_text(text: str, default: Optional[str] = None, /, **kwargs) -> str:
	default = default or ''
  
	def repl(match: re.Match) -> str:
		result = kwargs.get(match['key'], default)
                
		if not isinstance(result, str):
			return str(result)

		return result

	return re.sub(r'(?<!\\)\$(?P<key>[\w_]+)', repl, text, flags=re.IGNORECASE)

@overload
def in_range(num: int, range: tuple[float, float]) -> int: ...
@overload
def in_range(num: float, range: tuple[float, float]) -> float: ...
def in_range(num: Union[float, int], range: tuple[float, float]) -> Union[float, int]:
	min_n = min(range)
	max_n = max(range)

	return num >= min_n and num <= max_n

def find(iter: Iterable[T], check: Callable[[T], bool]) -> Generator[T, None, None]:
  return (item for item in iter if check(item))

def get(iter: Iterable[T], check: Callable[[T], bool]) -> Union[T, None]:
  return next(find(iter, check), None)

def is_empty_text(text: str) -> bool:
  return not text.strip()

def strip_text(
  text: str, *,
  ignore_accents:   Optional[bool] = None,
  ignore_empty:     Optional[bool] = None,
  case_insensitive: Optional[bool] = None,
  strip_text:       Optional[bool] = None,
  empty: 						Optional[str]  = None
) -> str:
  if is_empty_text(text):
    return text
  
  empty = empty if empty is not None else '-'
  
  if strip_text:
    text = text.strip()

  if ignore_accents:
     text = unidecode(text)

  if ignore_empty:
     text = re.sub(r'\s+', empty, text)
  
  if case_insensitive:
     text = text.lower()

  return text

def fmt(text: str, *, empty: Optional[str] = None) -> str:
  return strip_text(
     text=text,
     ignore_accents=True,
     ignore_empty=True,
     case_insensitive=True,
     strip_text=True,
     empty=empty
  )

def created_at(obj: Snowflake) -> datetime:
	timestamp = ((obj.id >> (MORKATO_SNOWFLAKE_BITS + MORKATO_SNOWFLAKE_SEQ)) + MORKATO_EPOCH) / 1000 # /1000 -> MS - SEG
     
	return datetime.fromtimestamp(timestamp)

def attack_format_discord(formatter: str, idx: int, attack: Attack, /, *args, **kwargs) -> str:
	kwargs.update(index=idx, attack=attack)
	text = formatter.format(*args, **kwargs)

	chunk = attack.children

	if not chunk:
		return text
  
	return '%s\n>  %s' % (text, '\n>  '.join(
    formatter.format(*args, **kwargs, index=idx, attack=atk)
    for (idx, atk) in enumerate(chunk, start=1)
  ))