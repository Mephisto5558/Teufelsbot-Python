# https://github.com/Mephisto5558/Teufelsbot/blob/main/Commands/Fun/happy.js

from secrets import choice

response_list = [
    'c:', 'C:', ':D',
    'https://tenor.com/view/yell-shout-excited-happy-so-happy-gif-17583147',
    'https://tenor.com/view/happy-cat-smile-cat-gif-26239281'
]

def happy():
  return choice(response_list)

if __name__ == '__main__': print(happy())