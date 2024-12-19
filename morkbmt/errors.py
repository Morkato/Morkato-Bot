from .extension import (Converter, Extension)
from typing import (
  Type,
  Any
)

class MorkatoBotManagerToolError(Exception): ...
class ValueNotInjectedError(MorkatoBotManagerToolError):
  def __init__(self, key: str, annotation: Any, /) -> None:
    super().__init__("Value for annotation: %s.%s it wasn't injected." % (annotation.__module__, annotation.__name__))
    self.key = key
    self.annotation = annotation
class ConverterNotInjectedError(MorkatoBotManagerToolError):
  def __init__(self, key: str, value: Type[Any], /) -> None:
    super().__init__("Converter: %s.%s (%s[%s]) it wasn't injected." % (value.__module__, value.__name__, Converter.__name__, value))
    self.key = key
    self.value = value
class ExtensionInvokeError(MorkatoBotManagerToolError):
  def __init__(self, extension: Extension, exception: Exception, /) -> None:
    super().__init__("Extension: %s.%s invoked a error: %s" % (extension.__module__, type(extension).__name__, exception))
    self.extension = extension
    self.exception = exception
class ConverterInvokeError(MorkatoBotManagerToolError):
  def __init__(self, converter: Converter[Any], exception: Exception, /) -> None:
    super().__init__("Converter: %s.%s invoked a error: %s" % (converter.__module__, type(converter).__name__, exception))
    self.converter = converter
    self.exception = exception