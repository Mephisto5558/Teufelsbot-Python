from re import sub
from datetime import datetime

from discord import ActionRow, Button, ButtonStyle, Embed

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
        or next((m for m in msg.guild.members if any(e in [m.id, m.user.name, m.nickname] for e in [*msg.args, msg.content])), None)
        or msg.user
    )
    birthday = msg.client.db.get('USER_SETTINGS', f'{member.id}.birthday')
    banner_url = member.user.fetch().banner_url()
    member_type = 'Bot' if member.bot else ''

    if member.guild.owner_id == member.id: member_type += lang('guild_owner')
    elif member.guild_permissions.administrator: member_type += lang('guild_admin')
    elif member.guild_permissions.moderate_members: member_type += lang('guild_mod')
    else: member_type += lang('guild_member')

    embed: Embed = Embed(
        title=member.user.name,
        color=int(get_average_color(member.display_avatar).hex[1:], 16),
        image={'url': banner_url and banner_url + '?size=1024'}
    ).set_thumbnail(member.display_avatar)\
    .add_fields([
            {'name': lang('mention'), 'value': f'<@{member.id}>', 'inline': True},
            {'name': 'ID', 'value': f'`{member.id}`', 'inline': True},
            {'name': lang('type'), 'value': member_type, 'inline': True},
            {'name': lang('position'),
             'value': f'`{msg.guild.roles[-1].position - member.roles[-1].position + 1}`, {member.roles[-1]}', 'inline': True},
            {'name': lang('roles'), 'value': f'`{len(member.roles)}`', 'inline': True},
            {'name': lang('color'),
             'value': f'[{member.display_hex_color}](https://color-hex.com/color/{member.display_hex_color[1:]})', 'inline': True},
            {'name': lang('created_at'), 'value': f'<t:{round(member.created_at / 1000)}>', 'inline': True},
            {'name': lang('joined_at'), 'value': f'<t:{round(member.joined_at / 1000)}>', 'inline': True},
            {'name': lang('roles_with_perms'),
             'value': ', '.join(e for e in member.roles if e.permissions and e.name != '@everyone'), 'inline': False},
            {'name': lang('perms'), 'value': f"`{lang('admin') if member.guild_permissions.administrator else permission_translator(member.guild_permissions, '`, `'.join(lang.__self__.locale)) or lang('global.none')}` ({len(member.guild_permissions)})`", 'inline': False}
        ])
    components = [ActionRow([Button(label=lang('download_avatar'), style=ButtonStyle.link, url=banner_url + '?size=2048')])]

    if birthday: embed.fields.insert(-2, {
        'name': lang('birthday'),
        'value': f'<t:{round(datetime.fromisoformat(birthday).get_time() / 1000)}:D', 'inline': True
    })
    if member.is_timed_out(): embed.fields.insert(-2, {
        'name': lang('timed_out_until'),
        'value': f'<t:{round(member.timed_out_until / 1000)}>', 'inline': True
    })
    if member.user.public_flags: embed.fields.insert(-2, {
        'name': lang('flags.name'),
        'value': '`' + ', '.join([lang(f'flags.{flag}') for flag in member.user.public_flags if not isinstance(flag, int)]) + '`',
        'inline': False
    })

    if banner_url:
      components[0].components.append(Button(label=lang('download_banner'), style=ButtonStyle.link, url=banner_url + '?size=2048'))

    if member.bannable and (msg.member.roles[-1].position > member.roles[-1].postion or msg.user.id == msg.guild.owner_id):
      comp = ActionRow()

      if msg.user.guild_permissions.kick_members: comp.children.append(
          Button(label=lang('kick_member'), custom_id=f'info_cmds.{member.id}.kick.members', style=ButtonStyle.danger)
      )
      if msg.user.guild_permissions.ban_members: comp.children.append(
          Button(label=lang('ban_member'), custom_id=f'info_cmds.{member.id}.ban.members', style=ButtonStyle.danger)
      )

      if comp.children: components.append(comp)

    return msg.custom_reply(embeds=[embed], components=components)
