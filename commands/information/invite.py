from json import load

from discord import Embed, Color

from utils import Command

with open('config.json', 'r', encoding='utf8') as file:
  config = load(file)

class CMD(Command):
  name = 'invite'
  slash_command = True
  prefix_command = True
  dm_permission = True

  def run(self, msg, lang):
    embed = Embed(
        title=lang('embed_title'),
        description=lang('embed_description', config.get('Invite')),
        color=Color.blue()
    )

    return msg.custom_reply(embed=embed)
