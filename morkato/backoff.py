from typing import Callable, Union

import random
import time

class Backoff:
  def __init__(self, base: int = 1):
    self._base: int = base

    self._exp: int = 0
    self._max: int = 10
    self._reset_time: int = base * 2**11
    self._last_invocation: float = time.monotonic()

    rand = random.Random()
    rand.seed()

    self._randfunc: Callable[..., Union[int, float]] = rand.randrange
  
  def delay(self) -> Union[int, float]:
    invocation = time.monotonic()
    interval = invocation - self._last_invocation
    self._last_invocation = invocation

    if interval > self._reset_time:
      self._exp = 0

    self._exp = min(self._exp + 1, self._max)
    return self._randfunc(0, self._base * 2**self._exp)