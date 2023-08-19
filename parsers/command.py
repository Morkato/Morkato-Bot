from typing import Union, Tuple

from .flag import parse as flag_parse

import pyparsing as pp
import re

name_syntax = pp.Regex(r'(?<![^&>-])[^&>-].*?[^&>-]?(?![^&>-])', re.IGNORECASE)

parser = pp.Forward() << name_syntax + pp.Optional(pp.Suppress(pp.Literal('--') | pp.Literal('>') | pp.Literal('->')) + pp.Regex(r'.*'))

params_syntax = r'@(?P<key>[a-z]+) (?P<value>\".*?\"|[^@]+)'

def extract_params(text: str) -> Tuple[str, dict[str, str]]:
  params = {}

  def repl(match: re.Match) -> str:
    params[match['key']] = match['value'] if not re.match(r'".*?"', match['value']) else match['value'][1:-1]

    return ''

  return (re.sub(params_syntax, repl, text, flags=re.IGNORECASE).strip(), params)

def is_empty(text: str) -> bool:
  return not text.strip()

def parse_result(result: pp.ParseResults) -> Tuple[Union[str, None], Union[str, None], dict[str, str]]:
  value, params = extract_params(result[0])

  value_in = ''

  if len(result) == 2:
    value_in, o_params = extract_params(result[1])

    params |= o_params

  return (
    value if not is_empty(value) else None,
    value_in if not is_empty(value_in) else None,
    params
  )

def parse(text: str) -> Tuple[Union[str, None], Union[str, None], Union[str, None], dict[str, str]]:
  """
    Doc
  """
  
  context = flag_parse(text)

  if not context.value:
    return (
      context.flag,
      None,
      None,
      {}
    )

  value, value_in, params = parse_result(parser.parseString(context.value))

  return (
    context.flag,
    value,
    value_in,
    params
  )