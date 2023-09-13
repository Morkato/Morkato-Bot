from typing import TypeVar, Union

import re

base_pattern = r'^\s*(-[a-z]|--[a-z]+)?([^-].*)?$'

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
    result = list(re.match(base_pattern, text, re.IGNORECASE).groups())
  except:
    return (None, {})

  params = {}

  if not result[0]:
    if not result[1]:
      return (None, params)

    flag = re.search(r'\s(-[a-z]|--[a-z]+)', result[1], re.IGNORECASE)

    if not flag:
      return (result[1], params)

    start, _ = flag.span()
    
    text = result[1][start+1:]

    _, params = parse(text)

    return (result[1][:start].strip() or None, params)
    
  result[0] = re.sub(r'^--?', '', result[0])

  if not result[1]:
    params[result[0]] = []

    return (None, params)
  else:
    param_value, other_params = parse(result[1])

    params[result[0]] = [param_value]
  
    return (None, sum_dict(params, other_params))