from utils import Aliases, Command, Option, Cooldowns
from utils.component_handler import rps_send_challenge

class CMD(Command):
  name = 'rps'
  aliases = Aliases(prefix=['rockpaperscissors'])
  cooldowns = Cooldowns(user=1000)
  slash_command = True
  prefix_command = True
  options = [Option(name='opponent', type='User')]

  def run(self, msg, lang):
    return rps_send_challenge(msg, msg.user, msg.options.get_member('opponent') or msg.args[0], lang)
