from __future__ import annotations
from typing_extensions import Self
from typing import (
  Iterator,
  SupportsInt,
  Tuple,
  Union,
  Type,
  Dict,
  Any
)
def make_flag_method(flag: int):
  def method(self: Flags):
    return self.hasflag(flag)
  return method
def get_flags(cls: Union[Type[Flags], Flags]) -> Dict[str, int]:
  return cls.__flags__
class FlagsMeta(type):
  __flags__: Dict[str, int]
  def __new__(cls, name: str, bases: Tuple[Any], attrs: Dict[str, Any], /, **kwargs) -> Any:
    annotations: Dict[str, Any] = attrs.get("__annotations__", {})
    flags: Dict[str, int]
    flags = attrs["__flags__"] = {}
    for (idx, (key, value)) in enumerate(annotations.items(), start=1):
      if isinstance(value, str):
        value = eval(value)
      if not issubclass(value, int):
        raise TypeError("Annotation of: %s is not :int:")
      flag = (1 << idx)
      attrs[key.lower()] = make_flag_method(flag)
      attrs[key.upper()] = flag
      flags[key] = flag
    return super().__new__(cls, name, bases, attrs, **kwargs)
class Flags(metaclass=FlagsMeta):
  @classmethod
  def all(cls) -> Self:
    all_flags = get_flags(cls(0)).values()
    flags_value = 0
    for flag_value in all_flags:
      flags_value |= flag_value
    return cls(flags_value)
  @classmethod
  def clean(cls, v: SupportsInt) -> Self:
    v = int(v)
    cleaned_value = 0
    all_flags: Iterator[int] = iter(get_flags(cls(0)).values())
    all_flags = (flag_value for flag_value in all_flags if (v & flag_value) != 0)
    for flag_value in all_flags:
      cleaned_value |= flag_value
    return cls(cleaned_value)
  def __init__(self, v: int) -> None:
    if self.__class__ is Flags:
      raise RuntimeError("Don't calling :Flags: class.")
    self.__value = v
  def __repr__(self) -> str:
    text = '<%s ' % self.__class__.__name__
    all_flags = get_flags(self).items()
    valid_flags = (name for (name, value) in all_flags if self.hasflag(value))
    text += ' '.join(valid_flags)
    text += '>'
    return text
  def __int__(self) -> int:
    return self.__value
  def __hash__(self):
    return self.__value
  def hasflag(self, flag: int, /) -> bool:
    return (self.__value & flag) != 0
  def isempty(self) -> bool:
    return self.__value == 0
  def copy(self) -> Self:
    return self.__class__(int(self.__value))
  def set(self, flag: int, /) -> None:
    all_flags = get_flags(self).values()
    if flag not in all_flags:
      raise ValueError("Invalid flag value: %s" % flag)
    self.__value |= flag