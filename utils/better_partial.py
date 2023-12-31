from functools import partial
from typing import Callable, Any

def better_partial(func: Callable, *args: Any, **kwargs: Any):
  """A wrapper for `functools.partial()` that adds `__self__` if exists"""

  partial_func = partial(func, *args, **kwargs)
  if hasattr(func, '__self__'): setattr(partial_func, '__self__', func.__self__)

  return partial_func
