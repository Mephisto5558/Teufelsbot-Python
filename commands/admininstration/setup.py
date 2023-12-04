from functools import partial

from discord import Embed, Color

from utils import Aliases, Command, Option, Cooldowns, Permissions, i18n_provider

backup = {'creator': 0, 'owner': 1, 'creator+owner': 2, 'admins': 3}
logger_action_types = ['message_delete', 'message_update', 'voice_channel_activity', 'say_command_used']

def get_cmds(client):
  return list({e.name for e in client.prefix_commands + client.slash_commands if not e.alias_of})

def autocomplete_language(i):
  return [
      {'name': i18n_provider.__('global.language_name', locale=k, none_not_found=True) or k, 'value': k}
      for k, v in i18n_provider.available_locales
      if i.focused.value.lower() in k.lower() or i.focused.value.lower() in v.lower()
  ][:25]


class CMD(Command):
  name = 'setup'
  aliases = Aliases(slash=['config'])
  permissions = Permissions(user=['manage_guild'])
  cooldowns = Cooldowns(user=1e4)
  slash_command = True
  prefix_command = False
  options = [
      Option(
          name='toggle_module',
          type='Subcommand',
          options=[Option(name='module', type='String', required=True, choices=['gatekeeper', 'birthday'])]
      ),
      Option(
          name='toggle_command',
          type='Subcommand',
          options=[
              Option(
                  name='command',
                  type='String',
                  required=True,
                  autocomplete_options=lambda i: get_cmds(i.client),
                  strict_autocomplete=True
              ),
              Option(name='get', type='Boolean'),
              (Option(name=f'role_{i+1}', type='Role') for i in range(6)),
              (Option(name=f'channel_{i+1}', type='Channel', channel_types=Constants.TextBasedChannelTypes) for i in range(6)),
              (Option(name=f'member_{i+1}', type='User') for i in range(6))
          ]
      ),
      Option(
          name='language',
          type='Subcommand',
          options=[Option(
              name='allowed_to_load',
              type='String',
              required=True,
              autocomplete_options=autocomplete_language,  # type: ignore
              strict_autocomplete=True,
          )]
      ),
      Option(
          name='autopublish',
          type='Subcommand',
          options=[Option(name='enabled', type='Boolean', required=True)]
      ),
      Option(
          name='logger',
          type='Subcommand',
          options=[
              Option(name='action', type='String', required=True, choices=['all', *logger_action_types]),
              Option(name='channel', type='Channel', channel_types=Constants.TextBasedChannelTypes),
              Option(name='enabled', type='Boolean')
          ]
      )
  ]

  async def run(self, msg, lang):
    match(msg.options.get_subcommand()):
      case 'toggle_module':
        module = msg.options.get_string('module')
        setting = msg.guild.db[f'{module}.enable']

        msg.client.db.set('GUILD_SETTINGS', f'{msg.guild.id}.{module}.enable', not setting)
        return msg.edit_reply(lang('toggled_module', name=module, state=lang('global.disabled' if setting else 'global.enabled')))

      case 'toggle_command':
        command = msg.options.get_string('command')
        command_data = msg.guild.db[f'command_settings.{command}.disabled'] or {}
        roles = command_data['roles'] or []
        channels = command_data['channels'] or []
        users = command_data['users'] or []
        count = {'enabled': {'channels': 0, 'users': 0, 'roles': 0}, 'disabled': {'channels': 0, 'users': 0, 'roles': 0}}

        if command not in get_cmds(msg.client): return msg.edit_reply(lang('toggle_cmd.not_found'))

        if msg.options.get_boolean('get'):
          fields = [
              {
                  'name': lang(f'toggle_cmd.{e[1]}'),
                  'inline': False,
                  'value': ', '.join(lang('toggle_cmd.list.all') if '*' in e[1] else [
                      f'<@&{e1}>' if e[0] == 'roles'
                      else f'<#{e1}>' if e[0] == 'channels'
                      else f'<@{e1}>'
                      for e1 in e[1]
                  ])
              }
              for e in [['roles', roles], ['channels', channels], ['users', users]]
              if e and e[1]
          ]
          embed = Embed(
              title=lang('toggle_cmd.list.embed_title', command),
              color=0,
              *({'fields': fields} if fields else {'description': lang('toggle_cmd.list.embed_description')})
          )

          return msg.edit_reply(embeds=[embed])

        if len(msg.options.data[0].options) == (2 if next(e for e in msg.options.data[0].options if e.name == 'get') else 1):
          msg.client.db.set(
              'GUILD_SETTINGS',
              f'{msg.guild.id}.command_settings.{command}.disabled.users',
              filter(lambda e: e != '*', users) if '*' in users else ['*', *users]
          )
          return msg.edit_reply(lang(f"toggle_cmd.{'enabled' if '*' in users else 'disabled'}", command))

        if '*' in users:
          return msg._edit_reply(lang('toggle_cmd.is_disabled', command=command, id=msg.command.id))

        for type_index, type_filter in enumerate(['role', 'member', 'channel']):
          ids = {e.value for e in msg.options.data[0].options if type_filter in e.name}
          type_ = 'roles'

          if type_index == 1: type_ = 'users'
          elif type_index == 2: type_ = 'channels'

          for id_ in ids:
            if id_ in command_data[type_]:
              command_data[type_] = [e for e in command_data[type_] if e != id_]
              count['enabled'][type_] += 1
              continue

            command_data[type_] = [*(command_data[type_] or []), id_]
            count['disabled'][type_] += 1

        embed = Embed(
            title=lang('toggle_cmd.embed_title', command),
            description=lang('toggle_cmd.embed_description', msg.command.id),
            fields=[{
                'name': lang(f'toggle_cmd.embed.{k}'),
                'value': '\n'.join([f"{lang(f'toggleCmd.{k}')}: **{v}**" for k, v in v.items() if v]),
                'inline': True
            } for k, v in count.items() if any(v.values())],
            color=0
        )

        msg.client.db.set('GUILD_SETTINGS', f'{msg.guild.id}.command_settings.{command}.disabled', command_data)
        return msg.edit_reply(embeds=[embed])

      case 'language':
        language = msg.options.get_string('language')
        new_lang = partial(
            i18n_provider.__, locale=language if language in i18n_provider.available_locales else i18n_provider.config.default_locale
        )
        cmd = msg.client.slash_commands.get(msg.command_name)
        embed = Embed(
            title=new_lang(f'commands.{cmd.category.lower()}.{cmd.name}language.embed_title'),
            description=new_lang(
                f'commands.{cmd.category.lower()}.{cmd.name}language.embed_description',
                args=str(new_lang('global.language_name'))
            ),
            color=Color.green()
        )

        msg.client.db.set('GUILD_SETTINGS', f'{msg.guild.id}.config.lang', language)
        return msg.edit_reply(embeds=[embed])

      case 'serverbackup':
        msg.client.db.set('GUILD_SETTINGS', 'serverbackup.allowed_to_load', int(backup[msg.options.get_string('allowed_to_load')]))
        return msg.custom_reply(lang('serverbackup.success'))

      case 'autopublish':
        enabled = msg.options.get_boolean('enabled')
        msg.client.db.set('GUILD_SETTINGS', f'{msg.guild.id}.config.autopublish', enabled)
        return msg.custom_reply(lang('autopublish.success', lang('global.enabled' if enabled else 'global.disabled')))

      case 'logger':
        action = msg.options.get_string('action')
        channel = (
            msg.options.get_channel('channel')
            or msg.guild.channels.get(msg.guild.db[f'config.logger.{action}.channel']) or {'id': None}
        )['id']
        if not channel: return msg.edit_reply(lang('logger.no_channel'))

        enabled = msg.options.get_boolean('enabled')
        if enabled is None and action != 'all': enabled = not msg.guild.db[f'config.logger.{action}.enabled']

        if action == 'all':
          if enabled is None: return msg.edit_reply(lang('logger.no_channel'))

          for action in logger_action_types:
            msg.client.db.set('GUILD_SETTINGS', f'{msg.guild.id}.config.logger.{action}', {'channel': channel, 'enabled': enabled})

        msg.client.db.set('GUILD_SETTINGS', f'{msg.guild.id}.config.logger.{action}', {'channel': channel, 'enabled': enabled})
        return msg.edit_reply(lang(
            'logger.enabled' if enabled
            else 'logger.disabled', {'channel': channel, 'action': lang(f'logger.actions.{action}')}
        ))
