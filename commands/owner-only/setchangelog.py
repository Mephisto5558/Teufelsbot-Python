from discord import Message

from utils import Command

class CMD(Command):
  name = 'setchangelog'
  slash_command = False
  prefix_command = True
  dm_permission = True

  async def run(self, msg: Message, lang):
    msg.client.db.set('BOT_SETTINGS', 'changelog', msg.content.replace('/n', '\n'))
    return msg.reply(lang('success'))
