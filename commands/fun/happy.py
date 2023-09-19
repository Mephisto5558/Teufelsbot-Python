from secrets import choice

from discord import Message

from utils import Command

response_list = [
    'c:', 'C:', ':D', 'Wuiiiii',
    'https://tenor.com/view/yell-shout-excited-happy-so-happy-gif-17583147',
    'https://tenor.com/view/happy-cat-smile-cat-gif-26239281'
]

class CMD(Command):
  name = 'happy'
  slash_command = False
  prefix_command = True
  dm_permission = True

  async def run(self, msg: Message, _):
    return msg.reply(choice(response_list))
