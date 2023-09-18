from utils import Command, Permissions

class CMD(Command):
  name = 'blacklistuser'
  slash_command = False
  prefix_command = True
  dm_permission = True

  def run(self, msg, lang):
    if not msg.args: return msg.reply(lang('no_input'))

    blacklist = msg.client.settings.get('blacklist', [])
    if msg.args[0] == 'off':
      if msg.args[1] not in blacklist: return msg.reply(lang('not_found'))

      msg.client.db.set('BOTSETTINGS', 'blacklist', [e for e in blacklist if e != msg.args[1]])
      return msg.reply(lang('removed', msg.args[1]))

    if msg.args[0] == msg.client.application.owner.id: msg.edit_reply(lang('cant_blacklist_owner'))

    blacklist.append(msg.args[0])
    msg.client.db.set('BOTSETTINGS', 'blacklist', blacklist)

    return msg.reply(lang('saved', msg.args[0]))
