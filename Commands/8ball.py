# https://github.com/Mephisto5558/Teufelsbot/blob/main/Commands/Fun/8ball.js

from datetime import datetime
from os import getcwd
import hashlib
from random import seed, choice

# https://github.com/Mephisto5558/Teufelsbot/blob/main/Locales/en/commands/fun.json#L11-L46
responseList = [
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

def eightBall(ask: bool=True):
  inputStr = input('Enter your question: ') if ask else None
  if not inputStr: return 'No question provided.'

  now = datetime.now()
  seedStr = f'{inputStr.lower()}_{getcwd()}_{now.year}-{now.month}-{now.day}'

  seed(int(hashlib.sha256(seedStr.encode()).hexdigest(), 16))
  
  return choice(responseList)


if __name__ == '__main__':
  try:
    while(1): print(eightBall())
  except KeyboardInterrupt: exit(0)