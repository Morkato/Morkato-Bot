import pyparsing as pp

base_pattern = r'^([^\s]+)$'
flag_patten = r'(?:^-(?P<key>[a-z])|--(?P<key>[^\s]+))$'

base = pp.Regex(base_pattern)
flag = pp.Regex()

