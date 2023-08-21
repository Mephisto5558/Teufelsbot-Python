from typing import Self, TypeVar  # pylint: disable = no-name-in-module # false positive in git action
_V = TypeVar('_V')

class FlatDict(dict):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def get(self, key: str, *default_values):
    """Return the value for key if key is in the dictionary, else the first not-None default."""

    for default_value in default_values:
      value = super().get(key, default_value)
      if value is not None: return value
    return default_values[-1]

  def __getitem__(self, key: str) -> str | None | Self:
    value = self
    for k in key.split('.'):
      if isinstance(value, dict): value = value.get(k)
      elif value is None: return None
      else: raise KeyError(key)
    return value

  def __setitem__(self, key: str, value: _V) -> _V:
    keys = key.split('.')
    last_key = keys.pop()
    target = self
    for k in keys:
      if k in target and not isinstance(target[k], dict) and k is not last_key:
        raise ValueError('Cannot overwrite data that is not at the end of the path')
      if k not in target: target[k] = {}
      target = target.get(k, {})

    target[last_key] = value
    return value
