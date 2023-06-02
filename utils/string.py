import re

def format(text: str, /, **kwergs) -> str:
  regex = re.compile(r"\$(?P<key>[^\d \t\n\/]+)")

  expected = regex.finditer(text)

  for match in expected:
    if match['key'] == '$':
      text = text.replace('$$', '$')

      continue
    text = text.replace(f'${match["key"]}', kwergs.get(match['key'], F'${match["key"]}'))

  return text

letters = {
  ' ': '( -)+',
  '-': '( -)+'
}

def transformRegex(text: str, case_insensitive: bool = False) -> re.Pattern:
  flags = re.IGNORECASE if case_insensitive else 0
  text = text.replace(' ', '')

  pattern = re.compile('\\b' + '( +)?'.join(letter for letter in text) + '\\b', flags)

  return pattern