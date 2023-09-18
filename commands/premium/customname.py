from utils import Aliases, Command, Option, Cooldowns, Permissions

class CMD(Command):
  name = 'customname'
  aliases = Aliases(prefix=['custom-name'])
  permissions = Permissions(client=[], user=[])
  cooldowns = Cooldowns(user=3e4)
  slash_command = True
  prefix_command = True
  dm_permission = True
  premium = True
  options = [
      Option(
          name='set',
          type='Subcommand',
          options=[
              Option(name='name', type='String', min_length=2, max_length=32, required=True),
              Option(name='global', type='Boolean')
          ]
      ),
      Option(
          name='get',
          type='Subcommand',
          options=[
              Option(name='target', type='User'),
              Option(name='global', type='Boolean')
          ]
      ),
      Option(
          name='clear',
          type='Subcommand',
          options=[Option(name='global', type='Boolean')]
      )
  ]

  def run(self, msg, lang):
    target = msg.options.get_member('target') or msg.mentions.members.first() or msg.member or msg.user
    global_ = msg.options.get_boolean('global')
    if global_ and target.user: target = target.user

    match msg.options.get_subcommand() or msg.args[0] or 'get':
      case 'clear':
        if target.custom_name:
          if global_: target.user.custom_name = None
          else: target.custom_name = None

        return msg.custom_reply(lang('clear.success'))

      case 'get':
        return msg.custom_reply(lang('get.success_you' if target.id == msg.user.id else 'get.success_other', target.custom_name))

      case 'set':
        new_name = msg.options.get_string('name') or ' '.join(msg.args[1:] if msg.args[0] == 'set' else msg.args)[:32] or None
        if global_: target.user.custom_name = new_name
        else: target.custom_name = new_name

        return msg.custom_reply(lang('set.success', new_name) if new_name else lang('clear.success'))
