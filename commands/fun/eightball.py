# https://github.com/Mephisto5558/Teufelsbot/blob/main/Commands/Fun/8ball.js

from datetime import datetime
from hashlib import sha256
from os import getcwd
from random import choice, seed
from sys import exit

# https://github.com/Mephisto5558/Teufelsbot/blob/main/Locales/en/commands/fun.json#L11-L46
response_list = [
    'As I see it, yes.',
    'It is certain.',
    'It is decidedly so.',
    'Most likely.',
    'Yes.',
    'Yesssss',
    'Yes – definitely.',
    'Your question delights me, my answer is: of course.',
    'You may rely on it.',
    'Outlook good.',
    'Signs point to yes.',
    'Without a doubt.',
    'Ask again later.',
    "I'm sorry, what? i wasn't listening.",
    'Better not tell you now.',
    'Cannot predict now.',
    'Concentrate and ask again.',
    'Reply hazy, try again.',
    'You ask to much.',
    "That's a secret.",
    "Don't count on it.",
    'Nope',
    'Nah',
    'No',
    'No.',
    'No!',
    'Noooooo!',
    'My reply is no.',
    'My sources say no.',
    'Outlook not so good.',
    'Very doubtful.',
    "I don't think so."
]

def eight_ball(ask: bool = True):
  input_str = input('Enter your question: ') if ask else None
  if not input_str: return 'No question provided.'

  now = datetime.now()
  seed_str = f'{input_str.lower()}_{getcwd()}_{now.year}-{now.month}-{now.day}'

  seed(int(sha256(seed_str.encode()).hexdigest(), 16))

  return choice(response_list)


if __name__ == '__main__':
  try:
    while True: print(eight_ball())
  except KeyboardInterrupt: exit()
