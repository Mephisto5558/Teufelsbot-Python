from utils import Command, Option, Permissions, ban_kick

class CMD(Command):
  name = 'ban'
  permissions = Permissions(client=['BanMembers'], user=['BanMembers'])
  slash_command = True
  prefix_command = False
  options = [
      Option(name='reason', type='String', required=True),
      Option(name='delete_days_of_messages', type='Number',min_value=1,max_value=7),
      Option(name='target', type='User')
      # Option(
        # name='duration',
        # type='String',
        # autocomplete_options: lambda i: time_validator(i.focused.value),
        # strict_autocomplete=True
      # )
  ]

  run = ban_kick
