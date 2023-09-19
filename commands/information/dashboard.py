from json import load

from discord import Embed

from utils import Aliases, Command

with open('config.json', 'r', encoding='utf8') as file:
  config = load(file)

class CMD(Command):
  name = 'dashboard'
  aliases = Aliases(prefix=['vote'], slash=['vote'])
  slash_command = True
  prefix_command = True
  dm_permission = True

  def run(self, msg, lang):
    embed = Embed(
        title=lang('embed_title'),
        description=(
            lang('embed_description_dashboard', config.get('Dashboard'))
            if msg.command_name == 'dashboard'
            else lang('embed_description_vote', f"{config.get('Domain')}/vote")
        )
    )

    return msg.custom_reply(embed=embed)
