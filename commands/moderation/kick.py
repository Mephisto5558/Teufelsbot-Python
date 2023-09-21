from utils import Command, Option, Permissions, ban_kick

class CMD(Command):
  name = 'kick'
  permissions = Permissions(client=['KickMembers'], user=['KickMembers'])
  slash_command = True
  prefix_command = False
  options = [
      Option(name='reason', type='String', required=True),
      Option(name='target', type='User')
  ]

  run = ban_kick
