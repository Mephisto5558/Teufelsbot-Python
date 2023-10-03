from json import load

from discord import Embed, Color

from utils import Command, Cooldowns, uptime

with open('config.json', 'r', encoding='utf8') as file:
  config = load(file)

class CMD(Command):
  name = 'uptime'
  cooldowns = Cooldowns(user=100)
  slash_command = True
  prefix_command = True
  dm_permission = True

  def run(self, msg, lang):
    embed = Embed(
        description=lang('embed_description', time=uptime(True, lang)['formatted'], Domain=config.get('Domain')),
        color=Color.white()
    )

    return msg.custom_reply(embed=embed)
