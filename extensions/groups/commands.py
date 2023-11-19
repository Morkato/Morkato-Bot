from typing import (
  Union,

  List,
  Dict
)

from morkato import (
  MorkatoContext,
  utils
)

import importlib.util

BaseType = Union[str, None]
ParamType = List[str]

class TestingGroupFlag(utils.FlagGroup):
  @utils.flag(name='i')
  async def iter(self, ctx: MorkatoContext, base: BaseType, param: ParamType, params: Dict[str, ParamType]) -> None:
    if base:
      await ctx.send(f'Don\'t implements options.')
    
    if not param:
      await ctx.send(f'Choose the module.')

      return
    
    spec = importlib.util.find_spec(param[0])

    if not spec:
      await ctx.send(f'Module: **`{param[0]}`** has not found.')

      return
    
    module = importlib.util.module_from_spec(spec)
    await ctx.send(f'Loading module from spec: **`{spec.name}`**')
    spec.loader.exec_module(module)
    await ctx.send(f'Memory module ID: **`{id(module)}`**')

    formatter = "$result"
    exec      = lambda: repr(module)

    if params.get('exec'):
      await ctx.send(f'Prepare loader for: **`{params["exec"][0]}`**')
      exec = getattr(module, params['exec'][0], None)
      
      if not exec:
        await ctx.send(f'Atribute: `{module.__name__}.{params["exec"][0]}` has not found, linked: **`repr`**')
        exec = lambda: repr(module)
    
    if params.get('formatter'):
      formatter = params["formatter"][0]
      await ctx.send(f'Setting formatter: \"{formatter}\"')
    
    r = exec()
    result = utils.format_text(formatter, result=str(r))

    await ctx.send(f'Result (Success): {result}')