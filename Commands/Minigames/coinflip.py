# https://github.com/Mephisto5558/Teufelsbot/blob/main/Commands/Minigames/coinflip.js

from random import random

def coin_flip():
  random_number = random()
  if random_number < 1 / 3000: return 'Side!'
  elif random_number < 0.5: return 'Heads'
  return 'Tail'


if __name__ == '__main__': print(coin_flip())
