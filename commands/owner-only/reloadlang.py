from discord import Message

from utils import Command, log, i18n_provider

class CMD(Command):
  name = 'reloadlang'
  slash_command = False
  prefix_command = True
  dm_permission = True
  beta = True

  async def run(self, msg: Message, lang):
    log.debug('Reloading language files, initiated by user %s', msg.user.name)

    i18n_provider.load_all_locales()
    return msg.reply(lang('success'))
