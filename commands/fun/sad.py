from secrets import choice

from discord import Message

from utils import Command

response_list = ['D:', ':c', 'qwq', ':C', 'q_q', ':/']

class CMD(Command):
  name = 'sad'
  slash_command = False
  prefix_command = True
  dm_permission = True

  async def run(self, msg: Message, _):
    return msg.custom_reply(content=choice(response_list))
