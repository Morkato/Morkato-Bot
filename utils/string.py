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