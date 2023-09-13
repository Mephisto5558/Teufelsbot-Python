from random import choices

from utils import Command

class CMD(Command):
  name = 'coinflip'
  slash_command = True
  prefix_command = True
  dm_permission = True

  def run(self, msg, lang):
    return msg.custom_reply(lang(choices(['response', 'side!'], weights=[1, 1 / 3000], k=1)[0]))
