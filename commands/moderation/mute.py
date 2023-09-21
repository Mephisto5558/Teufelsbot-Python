from datetime import datetime

from discord import DiscordException, Interaction, Embed, Color

from utils import Aliases, Command, Option, Permissions, time_validator, limit

class CMD(Command):
  name = 'mute'
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
          autocomplete_options=lambda i: time_validator(i.focused.value),
          strict_autocomplete=True
      )
  ]

  async def run(self, msg: Interaction, lang):
    target = msg.options.get_member('target')
    reason = msg.options.get_string('reason')
    duration = get_milliseconds(limit(msg.options.get_string('duration'), min_val=6e4, max_val=2419e5))
    date = datetime.now()

    if not target: return msg.response.edit_message(content=lang('not_found'))
    if target.id == msg.user.id: return msg.response.edit_message(content=lang('cant_mute_self'))
    if target.roles[-1].position - msg.user.roles[-1].position >= 0 and msg.guild.owner_id != msg.user.id:
      return msg.response.edit_message(content=lang('global.no_perm_user'))
    if target.guild_permissions.administrator: return msg.response.edit_message(content=lang('target_is_admin'))
    if not target.moderatebale: return msg.response.edit_message(content=lang('global.no_perm_bot'))
    if not duration or isinstance(duration, str): return msg.response.edit_message(content=lang('invalid_duration'))

    date.set_time(date.get_time() + duration)

    try: await target.timeout(until=date.get_time(), reason=f"{reason} | {lang('global.mod_reason', command=msg.command_name, user=msg.user.name)}")
    except DiscordException as err: return msg.response.edit_message(content=lang('error', str(err)))  # todo

    embed = Embed(
        title=lang('dm_embed_title'),
        description=lang(
            'dm_embed_description', guild=msg.guild.name, mod=msg.user.name, reason=reason,
            time=round(target.timed_out_until / 1000)
        ),
        color=Color.red()
    )

    no_msg = False
    try: target.send(embeds=[embed])
    except DiscordException: no_msg = True

    embed.title = lang('info_embed_title')
    embed.description = lang(
        'info_embed_description', user=target.user.name, reason=reason,
        time=round(target.timed_out_until / 1000)
    )
    if no_msg: embed.description += lang('no_dm')

    return msg.response.edit_message(embed=embed)
