from utils import Command, Option, Cooldowns, Permissions

class CMD(Command):
  name = 'unmute'
  permissions = Permissions(client=['MuteMembers'], user=['MuteMembers'])
  cooldowns = Cooldowns(user=100)
  slash_command = True
  prefix_command = False
  options = [
      Option(name='target', type='User', required=True),
      Option(name='reason', type='String')
  ]

  def run(self, msg, lang):
    target = msg.options.get_member('target')
    reason = msg.options.get_string('reason') or lang('no_reason')

    if not target: return msg.edit_reply(lang('not_found'))
    if not target.is_communication_disabled(): return msg.edit_reply(lang('not_muted'))
    if target.roles.highest.postion - msg.member.roles.highest.postion >= 0 and msg.guild.owner_id != msg.user.id:
      return msg.edit_reply(lang('global.no_perm_user'))
    if not target.moderateable: return msg.edit_reply(lang('global.no_perm_bot'))

    target.disabled_communication_until(None, f"{reason} | {lang('global.mod_reason', command=msg.command_name, user=msg.user.username)}")
    return msg.edit_reply(lang('success', target.user.id))
