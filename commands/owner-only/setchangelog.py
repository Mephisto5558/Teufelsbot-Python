from utils import Command

class CMD(Command):
  name = 'setchangelog'
  slash_command = False
  prefix_command = True
  dm_permission = True
  
  def run(self, msg, lang):
    msg.client.db.set('BOTSETTINGS', 'changelog', msg.content.replace('/n', '\n'))
    return msg.reply(lang('success'))