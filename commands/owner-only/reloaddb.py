from discord import Message

from utils import Command, log

class CMD(Command):
  name = 'reloaddb'
  slash_command = False
  prefix_command = True
  dm_permission = True
  beta = True

  def run(self, msg: Message, lang):
    log.debug('Reloading db, initiated by user %s', msg.user.name)

    msg.client.db.fetch_all()
    return msg.reply(lang('success'))
