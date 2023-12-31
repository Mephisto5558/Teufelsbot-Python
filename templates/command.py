# pylint: skip-file #type: ignore
from utils import Aliases, Command, Option, Cooldowns, Permissions

class CMD(Command):
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

  async def run(self, msg, lang):
    pass
