# https://github.com/Mephisto5558/Teufelsbot/blob/main/Utils/uptime.js

# pip install psutil
from psutil import Process
from math import floor
from time import time

process = Process()

# in a real-world example, this would work with I18n and language files
langData = {
  'dhms': '{d} Tagen, {h} Stunden, {m} Minuten und {s} Sekunden',
  'hms': '{h} Stunden, {m} Minuten und {s} Sekunden',
  'ms': '{m} Minuten und {s} Sekunden',
  's': '{s} Sekunden'
}

def lang(id: str, **keyword_params):
  str = langData[id]
  
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
    'formatted': lang(id, d=d, h=h, m=m, s=s) if id else '{:02}:{:02}:{:02}:{:02}'.format(d, h, m, s)
  }
  
if __name__ == '__main__': print(uptime(True))