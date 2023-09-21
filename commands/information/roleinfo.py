from re import sub

from discord import ActionRow, Embed, Button, ButtonStyle

from utils import Aliases, Command, Option, Cooldowns, permission_translator

class CMD(Command):
  name = 'roleinfo'
  aliases = Aliases(prefix=['role-info'])
  cooldowns = Cooldowns(user=1000)
  slash_command = True
  prefix_command = True
  options = [Option(name='role', type='Role')]

  def run(self, msg, lang):
    msg.args = [sub(r'/[<@>]/g', '', e) for e in msg.args]
    msg.content = sub(r'/[<@>]/g', '', msg.content)

    role = msg.options.get_role('role') or (msg.mentions.roles.first() if msg.args[0] else msg.member.roles.highest) or next(
        (r for r in msg.guild.roles.cache if r.id in [*msg.args, msg.content] or r.name in [*msg.args, msg.content]), None)
    if not role: return msg.custom_reply(content=lang('not_found'))

    embed = Embed(
        title=role.name,
        color=role.color
    ).add_field([
        {'name': lang('mention'), 'value': str(role), 'inline': True},
        {'name': lang('members'), 'value': len(role.members), 'inline': True},
        {
            'name': lang('color'),
            'value': f'[{role.hex_color}](https://color-hex.com/color/{role.hex_color[1:]})' if role.color else lang('global.none'),
            'inline': True
        },
        {'name': lang('mentionable'), 'value': lang(f'global.{role.mentionable}'), 'inline': True},
        {'name': lang('hoist'), 'value': lang(f'global.{role.hoist}'), 'inline': True},
        {'name': lang('managed'), 'value': lang(f'global.{role.managed}'), 'inline': True},
        {'name': lang('position'), 'value': f'`{msg.guild.roles.highest.position - role.position + 1}`', 'inline': True},
        {'name': 'ID', 'value': f'`{role.id}`', 'inline': True},
        {'name': lang('createdAt'), 'value': f'<t:{round(role.created_timestamp / 1000)}>', 'inline': True},
        {'name': lang('permissions'), 'inline': True}
    ])

    if role.guild_permissions.administrator:
      embed.fields[-1].value = f"`{lang('admin')}` (`{len(role.permissions)}`)"
    else:
      perms = '`, `'.join(permission_translator(role.permissions, lang.__self__.locale)) or lang('global.none')
      perms_str = f'`{perms}`' if len(perms) < 1017 else f"`{perms[:perms[:1013]].rfind(',')}...`"

      embed.fields[-1].value = f'{perms_str} (`{len(role.permissions.to_Array())}`)'

    if role.members and len(role.members) < 16:
      embed.fields.insert(9, {'name': lang('members'), 'value': ', '.join(role.members.values()), 'inline': False})

    if role.color:
      embed.thumbnail.url = f'https://dummyimage.com/80x80/{role.hex_color[1:]}/${role.hexColor[1:]}.png'
    elif role.icon:
      embed.thumbnail.url = f'https://cdn.discordapp.com/role-icons/{role.guild.id}/{role.icon}.webp?size=80&quality=lossless'

    if msg.member.guild_permissions.manage_roles and role.editable and (
        msg.member.roles[-1].position > role.position or msg.user.id == msg.guild.owner_id
    ):
      components = ActionRow([Button(label=lang('delete'), custom_id=f'info_cmds.{role.id}.delete.roles', style=ButtonStyle.danger)])
    else:
      components = None

    return msg.custom_reply(embed=embed, components=[components])
