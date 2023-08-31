# https://github.com/Mephisto5558/Teufelsbot/blob/main/Utils/uptime.js

from math import floor
from time import time

from psutil import Process

process = Process()

def uptime(as_message, lang):
  up = time() - process.create_time()
  d = floor(up / (60 * 60 * 24))
  h = floor((up / (60 * 60)) % 24)
  m = floor((up / 60) % 60)
  s = floor(up % 60)

  if as_message:
    if d: id_ = 'dhms'
    elif h: id_ = 'hms'
    elif m: id_ = 'ms'
    else: id_ = 's'
  else: id_ = None

  return {
      'total': up * 1000,
      'formatted': lang(id_, d=d, h=h, m=m, s=s) if id_ else f'{d:02}:{h:02}:{m:02}:{s:02}'
  }
