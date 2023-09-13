from utils import Command, Aliases, Permissions, Cooldowns, Option

class CMD(Command):
  name = 'tictactoe'
  aliases = Aliases(slash=['ttt'])
  permissions = Permissions(client=['manage_messages'])
  cooldowns = Cooldowns(user=5000)
  slash_command = True
  prefix_command = False
  options = [Option(name='opponent', type='user')]
  disabled = True  # game not implemented yet

  def run(self, msg, lang):
    target = msg.options.get_user('opponent')
    if target: target = target.id
