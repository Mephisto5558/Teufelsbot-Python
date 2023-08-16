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

def lang(id: str, **keyword_params):
  str = lang_data[id]

  if str is None: return None
  if keyword_params is None: return str
  return str.format(**keyword_params)

def uptime(as_message):
  up = time() - process.create_time()
  d = floor(up / (60 * 60 * 24))
  h = floor((up / (60 * 60)) % 24)
  m = floor((up / 60) % 60)
  s = floor(up % 60)

  id = None
  if as_message:
    if d: id = 'dhms'
    elif h: id = 'hms'
    elif m: id = 'ms'
    else: id = 's'

  return {
      'total': up * 1000,
      'formatted': lang(id, d=d, h=h, m=m, s=s) if id else f'{d:02}:{h:02}:{m:02}:{s:02}'
  }


if __name__ == '__main__': print(uptime(True))
