from __future__ import annotations
from typing_extensions import Self
from typing import (
  TYPE_CHECKING,
  Optional,
  Generic,
  TypeVar,
  Tuple,
  Union,
  Type,
  Dict,
  Any
)
if TYPE_CHECKING:
  from discord.interactions import Interaction
  from .context import MorkatoContext

T = TypeVar('T')
P = TypeVar('P')

class ConverterHandlerMeta(type):
  __converter_name__: str
  __registry_class__: bool
  def __new__(cls, name: str, bases: Tuple[Any], attrs: Dict[str, Any], /, **kwargs) -> Self:
    name = kwargs.pop("name", name)
    attrs["__converter_name__"] = name
    attrs["__registry_class__"] = False
    return super().__new__(cls, name, bases, attrs, **kwargs)
class Converter(Generic[P, T], metaclass=ConverterHandlerMeta):
  __converter_name__: str
  __registry_class__: bool
  def __init__(self) -> None: ...
  async def validate(self, arg: str) -> P:
    return arg
  async def convert(self, ctx: Union[MorkatoContext, Interaction], arg: P) -> T:
    raise NotImplementedError
  async def setup(self) -> None: ...
  async def close(self) -> None: ...
class ConverterManager:
  def __init__(self) -> None:
    self.loaded: Dict[Type[Any], Converter[Any, Any]] = {}
  async def convert(self, converter: Type[Converter[P, T]], ctx: Union[Interaction, MorkatoContext], arg: str, /, **kwargs) -> T:
    if not issubclass(converter, Converter):
      raise NotImplementedError
    loaded_converter: Optional[Converter[P, T]] = self.loaded.get(converter)
    if loaded_converter is None:
      raise NotImplementedError
    validated_argument = await loaded_converter.validate(arg)
    converted = await loaded_converter.convert(ctx, validated_argument, **kwargs)
    return converted