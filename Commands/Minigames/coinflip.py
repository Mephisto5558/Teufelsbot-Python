# https://github.com/Mephisto5558/Teufelsbot/blob/main/Commands/Minigames/coinflip.js

from random import random

def coinFlip():
  randomNumber = random()
  if randomNumber < 1/3000:
    return 'Side!'
  elif randomNumber < 0.5:
    return 'Heads'
  
  return 'Tail'

if __name__ == '__main__': print(coinFlip())