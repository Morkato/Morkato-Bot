from typing import (
  Optional,
  Iterator,
  Callable,
  Iterable,
  TypeVar,
  Tuple,
  Dict,
  List,
  Any
)
from .abc import (
  UnresolvedSnowflakeList,
  Snowflake
)
from collections import OrderedDict
from types import MappingProxyType
from datetime import datetime
import inspect

MORKATO_EPOCH = 1716973200000
DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
T_SNOWFLAKE = TypeVar('T_SNOWFLAKE', bound='Snowflake')
T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

class _MissingSpecialType:
  __slots__ = ()
  def __eq__(self, other: Any) -> bool:
    return False
  def __bool__(self) -> bool:
    return False
  def __hash__(self) -> int:
    return 0
  def __repr__(self) -> str:
    return "<Missing ...>"
MISSING: Any = _MissingSpecialType()
del _MissingSpecialType
class CircularDict(OrderedDict[K, V]):
  def __init__(self, maxlen: int) -> None:
    self.maxlen = maxlen
  def __getitem__(self, key: K) -> V:
    return OrderedDict.__getitem__(self, key)
  def __setitem__(self, key: K, value: V) -> None:
    OrderedDict.__setitem__(self, key, value)
    if len(self) > self.maxlen:
      self.popitem(last=False)
class NoNullDict(OrderedDict[K, V]):
  def __setitem__(self, key: K, value: V) -> None:
    if value is None:
      return
    super().__setitem__(key, value)
class UnresolvedSnowflakeListImpl(UnresolvedSnowflakeList[T_SNOWFLAKE]):
  def __init__(self) -> None:
    self.clear()
  def __iter__(self) -> Iterator[T]:
    return iter(self.items.values())
  def __len__(self) -> int:
    return len(self.items)
  def clear(self) -> None:
    self.items: Dict[int, T_SNOWFLAKE] = {}
    self.__already_loaded = False
  def order(self) -> List[T]:
    return sorted(self, key=lambda item: item.id)
  def already_loaded(self) -> bool:
    return self.__already_loaded
  async def resolve_impl(self) -> None:
    raise NotImplementedError
  async def resolve(self) -> None:
    try:
      if self.already_loaded():
        return None
      self.__already_loaded = True
      return await self.resolve_impl()
    except Exception as exc:
      self.clear()
      raise exc
  def add(self, object: T, /) -> None:
    if self.__already_loaded:
      self.items[object.id] = object
  def remove(self, object: Snowflake, /) -> Optional[T]:
    if self.__already_loaded:
      return self.items.pop(object.id, None)
  def get(self, id: int, /) -> Optional[T]:
    if not self.__already_loaded:
      return None
    return self.items.get(id)
def extract_datetime_from_snowflake(snow: Snowflake) -> datetime:
  timestamp = MORKATO_EPOCH + (snow.id >> 23)
  return datetime.fromtimestamp(timestamp / 1000.0)
def parse_arguments(
  parameters: MappingProxyType[str, inspect.Parameter], *,
  key: Callable[[Any], Any],
  globals: Optional[Dict[str, Any]] = None
) -> Tuple[Iterable[Any], Dict[str, Any]]:
  kwargs = {}
  args = []
  for (idx, (name, parameter)) in enumerate(parameters.items()):
    annotation = parameter.annotation
    value: Any = None
    if annotation is None:
      raise NotImplementedError
    elif isinstance(annotation, str):
      annotation = eval(annotation, globals)
    value = key(annotation)
    if parameter.kind in (parameter.POSITIONAL_OR_KEYWORD, parameter.POSITIONAL_ONLY):
      args.append(value)
    else:
      kwargs[name] = value
  return (args, kwargs)
def run_function_by_annotation(function: Callable[..., T], key: Callable[[Any], Any]) -> T:
  signature = inspect.signature(function)
  parameters = signature.parameters
  (args, kwgs) = parse_arguments(parameters, key)
  return function(*args, **kwgs)