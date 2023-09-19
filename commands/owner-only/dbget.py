from json import dumps

from discord import Message

from utils import Command

class CMD(Command):
  name = 'dbget'
  slash_command = False
  prefix_command = True
  dm_permission = True
  beta = True

  def run(self, msg:Message, lang):
    result = msg.client.db.get(msg.args[0], msg.args[1])

    if not result: return msg.reply(lang('not_found'))
    return msg.reply(f'```json\n{dumps(result,indent=2)}\n')
