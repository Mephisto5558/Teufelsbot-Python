from utils import Command, git_pull

class CMD(Command):
  name = 'gitpull'
  slash_command = False
  prefix_command = True
  dm_permission = True
  beta=True

  def run(self, msg, lang):
    git_pull()
    return msg.reply(lang('success'))