# pylint: skip-file #type: ignore
from utils import Aliases, Command, Option, Cooldowns, Permissions

class CustomCommand(Command):
  name = ''
  aliases = Aliases(prefix=[], slash=[])
  permissions = Permissions(client=[], user=[])
  cooldowns = Cooldowns(guild=0, user=0)
  slash_command = True
  prefix_command = True
  dm_permission = True
  disabled = False
  no_defer = False
  ephemeral_defer = False
  options = [
      Option(),
      Option()
  ]

  def run(self, msg, lang):
    pass
