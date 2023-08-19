from typing import Optional, Union

import pyparsing as pp
import re

flag_syntax = pp.Suppress(pp.Literal('-')) + pp.Regex(r'[a-z]',  re.IGNORECASE) | pp.Suppress(pp.Literal('--')) + pp.Regex(r'[a-z]+', re.IGNORECASE)

parser = pp.Forward()

parser << (pp.Optional(flag_syntax) + pp.Regex(r'.*'))

class Context:
  def __init__(self, *, flag: Optional[str] = None, value: Optional[str] = None) -> None:
    self.__flag = flag
    self.__value = value
  
  def __repr__(self) -> str:
    if not self.flag:
      return self.value or ''
    
    if len(self.flag) == 1:
      return f'-{self.flag}' + (self.value or '')
    
    return f'--{self.flag}' + (' ' + self.value if self.value else '')
  
  @property
  def flag(self) -> Union[str, None]:
    return self.__flag
  
  @property
  def value(self) -> Union[str, None]:
    return self.__value

def is_empty(text: str) -> bool:
  return not re.match(r'\s*', text)

def parse_result(result: pp.ParseResults) -> Context:
  if len(result) == 1:
    return Context(value=result[0] if not is_empty(result[0]) else None)
  
  return Context(flag=result[0], value=result[1] if not is_empty(result[1]) else None)

def parse(text: str) -> Context:
  """
    Doc
  """
  
  return parse_result(parser.parseString(text))
