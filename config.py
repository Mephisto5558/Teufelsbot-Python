import logging
from typing import Self, TypeVar # pylint: disable = no-name-in-module # false positive or smth
_V = TypeVar('_V')

############# LOGGER #############
logging.basicConfig(level=logging.DEBUG, datefmt='%Y-%m-%dZ%z %H:%M:%S')

class CustomFormatter(logging.Formatter):
  format_ = '%(asctime)s %(module)s#%(lineno)d: %(message)s'

  FORMATS = {
      logging.DEBUG: '\033[38;5;33m' + format_ + '\033[0m',
      logging.INFO: '\033[38;5;240m' + format_ + '\033[0m',
      logging.WARNING: '\033[38;5;226m' + format_ + '\033[0m',
      logging.ERROR: '\033[38;5;196m' + format_ + '\033[0m',
      logging.CRITICAL: '\033[1;31m' + format_ + '\033[0m'
  }

  def format(self, record):
    formatter = logging.Formatter(self.FORMATS.get(record.levelno))
    return formatter.format(record)

logger = logging.getLogger()

console_handler = logging.StreamHandler()
console_handler.setFormatter(CustomFormatter())
logger.handlers = [console_handler]


############# UN-FLATTENER #############

class FlatDict(dict):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def get(self, key: str, *default_values):
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
