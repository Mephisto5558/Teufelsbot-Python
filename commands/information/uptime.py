from json import load

from utils import Command, Cooldowns, uptime, Colors

with open('config.json', 'r', encoding='utf8') as file:
  config = load(file)

class CMD(Command):
  name = 'uptime'
  cooldowns = Cooldowns(user=100)
  slash_command = True
  prefix_command = True
  dm_permission = True

  def run(self, msg, lang):
    embed = EmbedBuilder(
        description=lang('embed_description', time=uptime(True, lang)['formatted'], Domain=config.get('Domain')),
        color=Colors.White
    )

    return msg.custom_reply(embeds=[embed])
