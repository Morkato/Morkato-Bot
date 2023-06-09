import re

import re

def format(text: str, /, *args, **kwargs) -> str:
  captured_variables = re.compile(r'\$(?P<key>[a-zA-Z_]+)').finditer(text)

  for captured in captured_variables:
    key = captured['key']

    if re.match('^[0-9]+$', key):
      try: value = args[int(key)]
      except: value = args[int(key) - len(args)]
    else:
      value = kwargs.get(key, '')

    start, end = captured.span()

    text = text.replace(f'${key}', value)

  return text.replace('$$', '$')

letters = {
  ' ': '( -)+',
  '-': '( -)+'
}

def transformRegex(text: str, case_insensitive: bool = False) -> re.Pattern:
  flags = re.IGNORECASE if case_insensitive else 0
  text = text.replace(' ', '')

  pattern = re.compile('\\b' + '( +)?'.join(letter for letter in text) + '\\b', flags)

  return pattern