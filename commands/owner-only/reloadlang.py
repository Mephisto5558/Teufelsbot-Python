from utils import Command, log, i18n_provider

class CMD(Command):
  name = 'reloadlang'
  slash_command = False
  prefix_command = True
  dm_permission = True
  beta=True

  def run(self, msg, lang):
    log.debug('Reloading language files, initiated by user %s', msg.user.username)

    i18n_provider.load_all_locales()
    return msg.reply(lang('success'))