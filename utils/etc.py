from typing import Optional, TypeVar, Union, overload
from numerize.numerize import numerize

from decouple import config

import pyparsing as pp
import re

T = TypeVar('T')

@overload
def getEnv(key: str) -> Union[str, None]: ...
@overload
def getEnv(key: str, default: T) -> Union[str, T]: ...
def getEnv(key: str, default: Optional[T] = None) -> Union[str, None, T]:
  try:
    return str(config(key))
  except:
    return default

var_or_func = pp.Word('$' + pp.alphanums + r' _+-/*^(,)\"\'')
if_not_exists = pp.Literal('?') + pp.Word('$' + pp.alphas + pp.alphanums + '+-/*^()')
conn = pp.Optional(pp.Literal(':') + var_or_func + pp.ZeroOrMore(if_not_exists))

sintax = var_or_func + pp.ZeroOrMore(if_not_exists) + conn

parser = pp.Forward()

parser << sintax

def sum_num(after: int | float, before: int | float, exp: str) -> int | float:
	if exp == '+':
		return after + before

	elif exp == '-':
		return after - before

	elif exp == '/':
		return after / before

	elif exp == '*':
		return after * before

def parse_exp(text: str, /, **kwargs) -> int | float:
  parsed = parser_exp.parseString(text)

  if len(parsed) == 1:
    match = parsed[0]

    if re.match(r'(?:\$(?P<name>[a-z0-9_]))', match, re.IGNORECASE):
      match = kwargs.get(match[1:], '0')
    if re.match(r'[0-9]+\.[1-9][0-9]+', parsed[0]):
      return float(parsed[0])

    return int(parsed[0])

  after, exp, before, others = (parse_exp(parsed[0]), parsed[1], parse_exp(parsed[2]), parsed[3:])

  result = sum_num(after, before, exp)

  if others:
    return sum_num(result, parse_exp(''.join(others[1:])), others[0])

  return result

def parse(text: str, /, **variables) -> str:
	parsed_text = [item for item in parser.parseString(text)]

	result = None
	
	if var_exp.match(parsed_text[0]) or re.match(r'(?:true|false|none)', parsed_text[0]):
		var = parsed_text[0][1:]

		result = variables.get(var)

	if not result and len(parsed_text) >= 3:
		try: index = parsed_text.index(':')
		except: index = -1
			
		if not index == -1:
			compiled_expr = compile(parsed_text[0], filename='<compile>', mode='eval')

			if eval(compiled_expr, {
				'__builtins__': {
				'num_fmt': numerize,
				'true': True,
				'false': False,
				'null': None
				}
			}):
				return parse(''.join(parsed_text[index+1:]), **variables)
			return parse(''.join(parsed_text[2:index]), **variables)
			
		elif parsed_text[1] == '?':
			return parse(''.join(parsed_text[2:]), **variables)
	
	elif re.match(r'^(\$[a-zA-Z_]+|[0-9+\-*/() ]|[A-Za-z_]+\([^)]+\))+$', parsed_text[0]):
		compiled_expr = compile(parsed_text[0], filename='<compile>', mode='eval')

		result = eval(compiled_expr, {
			'__builtins__': {
				'num_fmt': numerize
			}
		})
	
	return result or 'undefined'