# https://github.com/Mephisto5558/Teufelsbot/blob/main/Utils/uptime.js

from math import floor
from time import time
from psutil import Process

process = Process()

# in a real-world example, this would work with I18n and language files
lang_data = {
    'dhms': '{d} Tagen, {h} Stunden, {m} Minuten und {s} Sekunden',
    'hms': '{h} Stunden, {m} Minuten und {s} Sekunden',
    'ms': '{m} Minuten und {s} Sekunden',
    's': '{s} Sekunden'
}

def lang(id_: str, **keyword_params):
  str_ = lang_data[id_]

  if str_ is None: return None
  if keyword_params is None: return str_
  return str_.format(**keyword_params)

def uptime(as_message):
  up = time() - process.create_time()
  d = floor(up / (60 * 60 * 24))
  h = floor((up / (60 * 60)) % 24)
  m = floor((up / 60) % 60)
  s = floor(up % 60)

  id_ = None
  if as_message:
    if d: id_ = 'dhms'
    elif h: id_ = 'hms'
    elif m: id_ = 'ms'
    else: id_ = 's'

  return {
      'total': up * 1000,
      'formatted': lang(id_, d=d, h=h, m=m, s=s) if id_ else f'{d:02}:{h:02}:{m:02}:{s:02}'
  }


if __name__ == '__main__': print(uptime(True))
