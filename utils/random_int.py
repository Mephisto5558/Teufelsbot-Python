from secrets import randbelow
from sys import maxsize

def random_int(max_: int = maxsize + 1, min_: int = 0):
  """`max - min +1` must be greater then 0"""

  if min_ > max_: min_, max_ = max_, min_
  return randbelow(max_ - min_ + 1) + min_
