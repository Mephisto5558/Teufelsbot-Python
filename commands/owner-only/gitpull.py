from discord import Message

from utils import Command, git_pull

class CMD(Command):
  name = 'gitpull'
  slash_command = False
  prefix_command = True
  dm_permission = True
  beta = True

  async def run(self, msg: Message, lang):
    await git_pull()
    return msg.reply(lang('success'))
