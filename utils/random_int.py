from secrets import randbelow
from sys import maxsize


def random_int(max: int = maxsize + 1, min: int = 0):
  """`max - min +1` must be greater then 0"""
  if min > max: min, max = max, min
  return randbelow(max - min + 1) + min
