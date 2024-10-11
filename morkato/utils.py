from typing import (Optional, Callable, Iterable, TypeVar, Tuple, Dict, Any)
from collections import OrderedDict
from types import MappingProxyType
from datetime import datetime
from types import ModuleType
from .abc import Snowflake
from glob import glob
import importlib.util
import inspect
import os

MORKATO_EPOCH = 1716973200000
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
def extract_datetime_from_snowflake(snow: Snowflake) -> datetime:
  timestamp = MORKATO_EPOCH + (snow.id >> 23)
  return datetime.fromtimestamp(timestamp / 1000.0)
def parse_arguments(parameters: MappingProxyType[str, inspect.Parameter], *, key: Callable[[Any], Any], globals: Optional[Dict[str, Any]] = None) -> Tuple[Iterable[Any], Dict[str, Any]]:
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
def load_modules(source_dir: str) -> None:
  source = os.path.join(source_dir, "**/*.py")
  unloaded_modules = iter(glob(source, recursive=True))
  unloaded_modules = (source[:-3].replace('/', '.') for source in unloaded_modules)
  for module_name in unloaded_modules:
    module = ModuleType(module_name)
    spec = importlib.util.find_spec(module_name)
    if spec is None:
      raise ModuleNotFoundError(module_name)
    spec.loader.exec_module(module)