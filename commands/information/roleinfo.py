from re import sub

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
    if not role: return msg.custom_reply(lang('not_found'))

    embed = EmbedBuilder(
        title=role.name,
        color=role.color,
        fields=[
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
        ]
    )

    if PermissionFlagsBits.Administrator in role.permissions:
      embed.data.fields[-1].value = f"`{lang('admin')}` (`{len(role.permissions.to_array())}`)"
    else:
      perms = '`, `'.join(permission_translator(role.permissions.to_array, lang.__self__.locale)) or lang('global.none')
      perms_str = f'`{perms}`' if len(perms) < 1017 else f"`{perms[:perms[:1013]].rfind(',')}...`"

      embed.data.fields[-1].value = f'{perms_str} (`{len(role.permissions.to_Array())}`)'

    if role.members and len(role.members) < 16:
      embed.data.fields.insert(9, {'name': lang('members'), 'value': ', '.join(role.members.values()), 'inline': False})

    if role.color:
      embed.data.thumbnail.url = f'https://dummyimage.com/80x80/{role.hex_color[1:]}/${role.hexColor[1:]}.png'
    elif role.icon:
      embed.data.thumbnail.url = f'https://cdn.discordapp.com/role-icons/{role.guild.id}/{role.icon}.webp?size=80&quality=lossless'

    if PermissionFlagsBits.ManageRoles in msg.member.permissions and role.editable and (msg.member.roles.highest.position > role.position or msg.user.id == msg.guild.owner_id):
      components = [ButtonBuilder(label=lang('delete'), custom_id=f'info_cmds.{role.id}.delete.roles', style=ButtonStyle.Danger)]
    else:
      components = None

    return msg.custom_reply(embeds=[embed], components=components)
