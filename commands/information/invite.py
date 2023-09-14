from json import load

from utils import Command, Colors

with open('config.json', 'r', encoding='utf8') as file:
  config = load(file)

class CMD(Command):
  name = 'invite'
  slash_command = True
  prefix_command = True
  dm_permission = True

  def run(self, msg, lang):
    embed = EmbedBuilder(
        title=lang('embed_title'),
        description=lang('embed_description', config.get('Invite')),
        color=Colors.Blue
    )

    return msg.custom_reply(embeds=[embed])
