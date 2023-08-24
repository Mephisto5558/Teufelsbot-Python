# https://github.com/Mephisto5558/Teufelsbot/blob/main/Commands/Fun/advice.js

from requests import get


def advice():
  data = get('https://api.adviceslip.com/advice', timeout=10).json()
  return data['slip'].get('advice', None)


if __name__ == '__main__': print(advice())
