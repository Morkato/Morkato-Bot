from typing import (
  Callable,
  Coroutine,
  Union,
  
  Any
)

from discord.ext   import commands
from morkato.objects.guild import Guild


CoroNone = Coroutine[Any, Any, None]
StrOrNone = Union[str, None]

CommandFunction = Union[
  Callable[[
    commands.Context,
    Guild
  ], CoroNone],
  Callable[[
    commands.Context,
    Guild,
    Any
  ], CoroNone],
  Callable[[
    commands.Context,
    Guild,
    Any,
    StrOrNone
  ], CoroNone],
  Callable[[
    commands.Context,
    Guild,
    Any,
    StrOrNone,
    StrOrNone
  ], CoroNone],
  Callable[[
    commands.Context,
    Guild,
    Any,
    StrOrNone,
    StrOrNone,
    Union[dict[str, str], None]
  ], CoroNone]
]