from typing import Literal, Iterator, Union

from numerize.numerize import numerize
from discord.ext import commands
from unidecode import unidecode

import re

def get_captured_variables(text: str) -> Iterator[re.Match[str]]:
  return re.finditer(r'(?<!\\|\!)\$(?!\\|\!)(?P<key>[a-zA-Z_]+)', text)

def resolve_expression(exp: str, **kwargs) -> Union[str, None]:
  if re.match(r'^(\$[a-zA-Z_]+|[0-9+\-*/() ]|[A-Za-z_]+\([^)]+\))+$', exp):
    try:
      compiled_expr = compile(format_variables(exp, **kwargs), filename='<ast>', mode='eval')
      
      return str(eval(compiled_expr, {
        '__builtins__': {
          'sum': sum,
          'num_fmt': numerize,
          'case': lambda con, value, default: value if con else default,
          'null': None,
          'true': True,
          'false': False
        }
      }))

    except (SyntaxError, TypeError, ValueError) as err:
      print(err)

      return 'Error'

def format_variables(text: str, **kwargs) -> str:
  captured_variables = get_captured_variables(text)

  for captured in captured_variables:
    key = captured['key']

    value = kwargs.get(key, '')

    text = text.replace(f'${key}', value)
  
  return text.replace('\\$', '$')

def format_expressions(text: str, /, **kwargs) -> str:
  captured_expressions = re.finditer(r'!\$\((?P<expression>.+)\)', text)

  for captured in captured_expressions:
    expression = captured['expression'].strip()

    value = resolve_expression(expression)
      
    text = text.replace(f'!$({expression})', value or '')
  
  return text.replace('\\!$', '!$')

def format(text: str, /, **kwargs) -> str:
  text = format_variables(text, **kwargs)

  return format_expressions(text, **kwargs)

def toKey(text: str) -> str:
  return unidecode(text).strip(' ').lower().replace(' ', '-')

class Context(commands.Context):
  def __init__(self, ctx: commands.Context, result: dict) -> None:
    super().__init__(
      message=ctx.message,
      bot=ctx.bot,
      view=ctx.view,
      args=ctx.args,
      kwargs=ctx.kwargs,
      prefix=ctx.prefix,
      command=ctx.command,
      invoked_with=ctx.invoked_with,
      invoked_parents=ctx.invoked_parents,
      command_failed=ctx.command_failed,
      current_parameter=ctx.current_parameter,
      current_argument=ctx.current_argument,
      interaction=ctx.interaction
    )

    self.result = result

  def get_param(self, k: Literal[
    'param',
    'name',
    'value'
  ]) -> Union[str, None]:
    return self.result.get(k)

def parse_params(text: str) -> dict:
  """
    Parse parameters from the given text string.

    Args:
      text (str): The text to parse.

    Returns:
      dict: A dictionary containing the parsed parameters.

    Raises:
      None

    Examples:
      >>> parse_params("-p name > value")
      {'param': '-p', 'name': 'name', 'value': 'value'}

      >>> parse_params("param_name")
      {'param': None, 'name': 'param_name', 'value': None}
  """

  cap = re.match(r'(?:\s*(?P<name>[^&+>@].*?[^+>@](?![^+>@])))(?:\s*(?:>(?:\s(?P<value>.*))))?', text, re.IGNORECASE)

  if not cap:
    return { 'param': None, 'name': None, 'value': None }
  
  print(cap)

  
  name = cap['name'].strip()

  if name.startswith('-'):
    return {
      'param': name[1],
      'name': name[2:] or None,
      'value': cap['value']
    }
  
  return {
    'param': None,
    'name': name,
    'value': cap['value']
  }