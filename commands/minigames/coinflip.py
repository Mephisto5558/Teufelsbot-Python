# https://github.com/Mephisto5558/Teufelsbot/blob/main/Commands/Minigames/coinflip.js

from random import choices

def coin_flip():
  return choices(['Heads', 'Tail', 'Side!'], weights=[1, 1, 1 / 3000], k=1)[0]


if __name__ == '__main__': print(coin_flip())
