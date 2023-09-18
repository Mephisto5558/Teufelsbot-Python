from re import sub
from datetime import datetime

from utils import Aliases, Command, Option, Cooldowns, get_age, permission_translator

class CMD(Command):
  name = 'userinfo'
  aliases = Aliases(prefix=['user-info'])
  cooldowns = Cooldowns(user=1000)
  slash_command = True
  prefix_command = True
  options = [Option(name='target', type='User')]

  def run(self, msg, lang):
    msg.args = [sub(r'/[<@&>]/g', '', e) for e in msg.args]
    msg.content = sub(r'/[<@&>]/g', '', msg.content)

    member = (
        msg.options.get_member('target') or msg.mentions.members.first()
        or next((m for m in msg.guild.members.cache if any(e in [m.user.id, m.user.username, m.user.tag, m.nickname] for e in [*msg.args, msg.content])), None)
        or msg.member
    )
    birthday = msg.client.db.get('userSettings', f'{member.id}.birthday')
    banner_url = member.user.fetch().banner_url()
    member_type = 'Bot' if member.user.bot else ''

    if member.guild.owner_id == member.id: member_type += lang('guild_owner')
    elif PermissionFlagsBits.Administrator in member.permissions: member_type += lang('guild_admin')
    elif PermissionFlagsBits.ModerateMembers in member.permissions: member_type += lang('guild_mod')
    else: member_type += lang('guild_member')

    embed = EmbedBuilder(
        title=member.user.username,
        color=int(get_average_color(member.display_avatar_url()).hex[1:], 16),
        thumbnail={'url': member.display_avatar_url()},
        image={'url': banner_url and banner_url + '?size=1024'},
        fields=[
            {'name': lang('mention'), 'value': member.user.toString(), 'inline': True},
            {'name': 'ID', 'value': f'`{member.id}`', 'inline': True},
            {'name': lang('type'), 'value': member_type, 'inline': True},
            {'name': lang('position'),
             'value': f'`{msg.guild.roles.highest.position - member.roles.highest.position + 1}`, {member.roles.highest}', 'inline': True},
            {'name': lang('roles'), 'value': f'`{member.roles.cache.size}`', 'inline': True},
            {'name': lang('color'),
             'value': f'[{member.display_hex_color}](https://color-hex.com/color/{member.display_hex_color[1:]})', 'inline': True},
            {'name': lang('created_at'), 'value': f'<t:{round(member.user.created_timestamp / 1000)}>', 'inline': True},
            {'name': lang('joined_at'), 'value': f'<t:{round(member.joined_timestamp / 1000)}>', 'inline': True},
            {'name': lang('roles_with_perms'),
             'value': ', '.join(e for e in member.roles.cache.values()if e.permissions and e.name != '@everyone'), 'inline': False},
            {'name': lang('perms'), 'value': f"`{lang('admin') if PermissionFlagsBits.Administrator in member.permissions else permission_translator(member.permissions.toArray(), '`, `'.join(lang.__self__.locale)) or lang('global.none')}` ({len(member.permissions.toArray())})`", 'inline': False}
        ]
    )
    components = [ActionRowBuilder(
        components=[ButtonBuilder(label=lang('download_avatar'), style=ButtonStyle.Link, url=banner_url + '?size=2048')]
    )]

    if birthday: embed.data.fields.insert(-2, {
        'name': lang('birthday'),
        'value': f'<t:{round(datetime.fromisoformat(birthday).get_time() / 1000)}:D', 'inline': True
    })
    if member.is_communication_disabled(): embed.data.fields.insert(-2, {
        'name': lang('timed_out_until'),
        'value': f'<t:{round(member.communication_disabled_until_timestamp / 1000)}>', 'inline': True
    })
    if member.user.flags: embed.data.fields.insert(-2, {
        'name': lang('flags.name'),
        'value': '`' + ', '.join([lang(f'flags.{flag}') for flag in member.user.flags.to_array() if not isinstance(flag, int)]) + '`',
        'inline': False
    })

    if banner_url:
      components[0].components.append(ButtonBuilder(label=lang('download_banner'), style=ButtonStyle.Link, url=banner_url + '?size=2048'))

    if member.bannable and (msg.member.roles.highest.position > member.roles.highest.postion or msg.user.id == msg.guild.owner_id):
      comp = ActionRowBuilder()

      if PermissionFlagsBits.KickMembers in msg.member.permissions: comp.components.append(
          ButtonBuilder(label=lang('kick_member'), custom_id=f'info_cmds.{member.id}.kick.members', style=ButtonStyle.Danger)
      )
      if PermissionFlagsBits.BanMembers in msg.member.permissions: comp.components.append(
          ButtonBuilder(label=lang('ban_member'), custom_id=f'info_cmds.{member.id}.ban.members', style=ButtonStyle.Danger)
      )

      if comp.components: components.append(comp)

    return msg.custom_reply(embeds=[embed], components=components)
