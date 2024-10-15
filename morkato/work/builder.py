from typing import (
  Optional,
  Dict,
  Any
)
import os.path
import yaml

class MessageBuilderException(Exception): ...
class UnknownMessageContent(MessageBuilderException):
  def __init__(self, language: str, key: str) -> None:
    super().__init__("Unknown message content for key: %s.%s" % (language, key))
    self.language = language
    self.key = key
class KeyAlreadyExists(MessageBuilderException):
  def __init__(self, language: str, key: str, value: str) -> None:
    super().__init__("Key: %s in language: %s already exists. This is value: %s" % (key, language, value))
    self.language = language
    self.key = key
    self.value = value
class MessageBuilder:
  PT_BR = "ptBR"
  EN_US = "enUS"
  def __init__(self, base: Optional[str] = None) -> None:
    self.messages: Dict[str, Dict[str, str]] = {}
    self.base = base or '.'
  def get_content_unknown_formatting(self, language: str, key: str) -> str:
    try:
      builder = self.messages[language]
      content = builder[key]
      return content
    except KeyError:
      raise UnknownMessageContent(language, key)
  def get_content(self, language: str, key: str, /, *args, **parameters) -> str:
    content = self.get_content_unknown_formatting(language, key)
    return (content % args).format(**parameters)
  def safe_get_content_unknown_formatting(self, language: str, key: str) -> str:
    try:
      return self.get_content_unknown_formatting(language, key)
    except UnknownMessageContent as exc:
      return exc.args[0]
  def safe_get_content(self, language: str, key: str, /, *args, **parameters) -> str:
    try:
      return self.get_content(language, key, *args, **parameters)
    except UnknownMessageContent as exc:
      return exc.args[0]
  def from_archive(self, local: str, /) -> None:
    local = os.path.join(self.base, local)
    languages: Optional[Dict[str, Any]] = None
    with open(local, 'r') as fp:
      languages = yaml.safe_load(fp)
    for (language, obj) in languages.items():
      self.extend(language, obj)
  def set_content(self, language: str, key: str, value: str) -> None:
    builder = self.messages.get(language)
    if builder is None:
      builder = self.messages[language] = {}
    content = builder.get(key)
    if content is not None:
      raise KeyAlreadyExists(language, key, content)
    builder[key] = value
  def extend(self, language: str, obj: Dict[str, Any]) -> None:
    for (key, value) in obj.items():
      if not isinstance(value, str):
        raise TypeError("Don't supports for this type, supports for :str: only.")
      self.set_content(language, key, value)