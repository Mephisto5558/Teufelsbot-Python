from discord import Interaction

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

  async def run(self, msg: Interaction, lang):
    target = msg.options.get_member('target')
    reason = msg.options.get_string('reason') or lang('no_reason')

    if not target: return msg.response.edit_message(content=lang('not_found'))
    if not target.is_communication_disabled(): return msg.response.edit_message(content=lang('not_muted'))
    if target.roles.highest.postion - msg.member.roles.highest.postion >= 0 and msg.guild.owner_id != msg.user.id:
      return msg.response.edit_message(content=lang('global.no_perm_user'))
    if not target.moderateable: return msg.response.edit_message(content=lang('global.no_perm_bot'))

    target.disabled_communication_until(None, f"{reason} | {lang('global.mod_reason', command=msg.command_name, user=msg.user.name)}")
    return msg.response.edit_message(content=lang('success', target.user.id))
