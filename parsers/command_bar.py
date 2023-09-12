from typing import TypeVar, Union

import pyparsing as pp
import re

flag_syntax = pp.Suppress(pp.Literal('-')) + pp.Regex(r'[a-z]',  re.IGNORECASE) | pp.Suppress(pp.Literal('--')) + pp.Regex(r'[a-z]+', re.IGNORECASE)
base_syntax = pp.Regex(r'[^-].*')

parser = pp.Forward()

parser << pp.Optional(flag_syntax) + pp.Optional(base_syntax)

T = TypeVar('T')
K = TypeVar('K')

def sum_dict(dir1: dict[K, T], dir2: dict[K, T]) -> dict[K, T]:
  for key, value in dir1.items():
    if not key in dir2:
        continue
    
    dir1[key] = value + dir2.pop(key)

  return dir1 | dir2

def parse(text: str) -> tuple[Union[str, None], dict[str, str]]:
  result = None

  try:
    result = parser.parseString(text)
  except pp.ParseException:
    return (None, {})

  params = {}

  if len(result) == 1:
    flag = re.search(r'\s(-[a-z]|--[a-z]+)', result[0], re.IGNORECASE)

    if not flag:
      return (result[0], params)

    start, _ = flag.span()
    
    text = result[0][start+1:]

    _, params = parse(text)

    return (result[0][:start].strip(), params)
    
  if len(result) == 2:
    param_value, other_params = parse(result[1])

    params[result[0]] = [param_value]
  
    return (None, sum_dict(params, other_params))