from utils import Command, Permissions

class CMD(Command):
  name = 'selfrole'
  permissions = Permissions(client=['manage_members'], user=['manage_guild'])
  slash_command = True
  prefix_command = False
  ephemeral_defer = True

  async def run(self, msg, lang):
    return msg.custom_reply(lang('deprecated'))
