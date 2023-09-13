from secrets import choice

from utils import Command

response_list = ['D:', ':c', 'qwq', ':C', 'q_q', ':/']

class CMD(Command):
  name = 'sad'
  slash_command = False
  prefix_command = True
  dm_permission = True

  def run(self, msg, lang):
    return msg.custom_reply(choice(response_list))
