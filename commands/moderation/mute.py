from datetime import datetime

from utils import Aliases, Command, Option, Permissions, time_validator, limit, Colors

class CMD(Command):
  name = 'mute',
  aliases = Aliases(prefix=['timeout'], slash=['timeout'])
  permissions = Permissions(client=['MuteMembers'], user=['MuteMembers'])
  slash_command = True
  prefix_command = False
  options = [
      Option(name='target', type='User', required=True),
      Option(name='reason', type='String', required=True),
      Option(
        name='duration',
        type='String',
        autocomplete_options= lambda i: time_validator(i.focused.value),
        strict_autocomplete=True
      )
  ]

  def run(self, msg, lang):
    target = msg.options.get_member('target')
    reason=msg.options.get_string('reason')
    duration=get_milliseconds(limit(msg.options.get_string('duration'), min_val=6e4, max_val=2419e5))
    date = datetime.now()

    if not target: return msg.edit_reply(lang('not_found'))
    if target.id == msg.member.id: return msg.edit_reply(lang('cant_mute_self'))
    if target.roles.highest.compare_position_to(msg.member.roles.highest) > -1 and msg.guild.owner_id != msg.user.id:
      return msg.edit_reply(lang('global.no_perm_user'))
    if PermissionFlagsBits.Administrator in target.permissions: return msg.edit_reply(lang('target_is_admin'))
    if not target.moderateable: return msg.edit_reply(lang('global.no_perm_bot'))
    if not duration or isinstance(duration, str): return msg.edit_reply(lang('invalid_duration'))

    date.set_time(date.get_time() + duration)

    try: target.disable_communication_until(date.get_time(), f'{reason} | {lang('global.mod_reason', command=msg.command_name, user=msg.user.username)}')
    except Exception as err: return msg.edit_reply(lang('error', str(err)))

    embed = EmbedBuilder(
      title=lang('dm_embed_title'),
      description=lang('dm_embed_description', guild=msg.guild.name, mod=msg.user.tag, reason=reason, time=round(target.communication_disabled_until_timestamp / 1000)),
      color=Colors.Red
    )

    try: target.send(embeds=[embed])
    except: no_msg = True

    embed.data.title = lang('info_embed_title')
    embed.data.description = lang('info_embed_description', user=target.user.username, reason=reason, time=round(target.communication_disabled_until_timestamp /1000))
    if no_msg: embed.data.description += lang('no_dm')

    return msg.edit_Reply(embeds=[embed])