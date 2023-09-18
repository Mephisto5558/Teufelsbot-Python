from utils import Command, Option, Permissions, Colors

class CMD(Command):
  name = 'trigger'
  permissions = Permissions(user=['ManageMessages'])
  slash_command = True
  prefix_command = False
  options = [
      Option(
          name='add',
          type='Subcommand',
          options=[
              Option(name='trigger', type='String', required=True),
              Option(name='response', type='String', required=True),
              Option(name='wildcard', type='Boolean')
          ]
      ),
      Option(
          name='delete',
          type='Subcommand',
          options=[Option(
              name='query_or_id',
              type='String',
              autocomplete_options=lambda i: sorted(
                  [e for e in [trigger for trigger in i.guild.db.get('triggers', [])] if isinstance(e, str)] +
                  [e.trigger for e in [trigger for trigger in i.guild.db.get('triggers', [])] if isinstance(e, dict)],
                  key=lambda e: -1 if isinstance(e, str) else 1
              )
          )]
      ),
      Option(
          name='clear',
          type='Subcommand',
          options=[Option(name='confirmation', type='String', required=True)]
      ),
      Option(
          name='get',
          type='Subcommand',
          options=[
              Option(
                  name='query_or_id',
                  type='String',
                  autocomplete_options=lambda i: sorted(
                      [e for e in [trigger for trigger in i.guild.db.get('triggers', [])] if isinstance(e, str)] +
                      [e.trigger for e in [trigger for trigger in i.guild.db.get('triggers', [])] if isinstance(e, dict)],
                      key=lambda e: -1 if isinstance(e, str) else 1
                  )
              ),
              Option(name='short', type='Boolean')
          ]
      )
  ]

  def run(self, msg, lang):
    old_data = msg.guild.db.get('triggers') or []
    query = msg.options.get_string('query_or_id').lower()

    match msg.options.get_subcommand():
      case 'add':
        data = {
            'id': int(max([trigger['id'] for trigger in old_data], default=0)) + 1,
            'trigger': msg.options.get_string('trigger'),
            'response': msg.options.get_string('response').replace('/n', '\n'),
            'wildcard': msg.options.get_boolean('wildcard') or False
        }

        msg.client.db.set('GUILDSETTINGS', f'{msg.guild.id}.triggers', old_data + [data])
        return msg.edit_reply(lang('saved', data['trigger']))

      case 'delete':
        if query:
          trigger = next((trigger for trigger in old_data if trigger['id'] == query or trigger['trigger'].lower() == query), None)
        else:
          trigger = max(old_data, key=lambda trigger: trigger['id'], default={})
        if not trigger:
          return msg.edit_reply(lang('not_found'))
        filtered = [t for t in old_data if t['id'] != trigger['id']]
        if len(filtered) == len(old_data):
          return msg.edit_reply(lang('id_not_found'))
        msg.client.db.set('GUILDSETTINGS', f'{msg.guild.id}.triggers', filtered)
        return msg.edit_reply(lang('deleted_one', trigger['id']))

      case 'clear':
        confirmation = msg.options.get_string('confirmation').lower()
        if confirmation != lang('confirmation'): return msg.edit_reply(lang('needConfirm'))

        if not old_data:
          return msg.edit_reply(lang('none_found'))
        msg.client.db.delete('GUILDSETTINGS', f'{msg.guild.id}.triggers')
        return msg.edit_reply(lang('deleted_all', len(old_data)))

      case 'get':
        if not old_data:
          return msg.edit_reply(lang('none_found'))
        embed = EmbedBuilder(title=lang('embed_title'), color=Colors.Blue)
        if query or query == 0:
          trigger = next((trigger for trigger in old_data if trigger['id'] == query or trigger['trigger'].lower() == query), None)
          if not trigger: return msg.edit_reply(lang('not_found'))
          embed.title = lang('embed_title_one', trigger['id'])
          embed.description = lang('embed_description_one', {
              'trigger': trigger['trigger'][:1900],
              'response': trigger['response'][:1900],
              'wildcard': bool(trigger['wildcard'])
          })
        elif msg.options.get_boolean('short'):
          embed.description = lang('first_25') if len(old_data) > 25 else ' '
          embed.fields = [{
              'name': lang('short_field_name', trigger['id']),
              'inline': True,
              'value': lang('short_field_value', {
                  'trigger': trigger['trigger'][:200],
                  'response': trigger['response'][:200],
                  'wildcard': bool(trigger['wildcard'])
              })
          } for trigger in old_data[:25]]
        else:
          embed.description = ''.join([
              lang('long_embed_description', {
                  'id': trigger['id'],
                  'wildcard': bool(trigger['wildcard']),
                  'trigger': trigger['trigger'][:20],
                  'response': trigger['response'][:20]
              })
              for trigger in old_data
              if len(embed.description) < 3800
          ])
          return msg.edit_reply(embeds=[embed])
