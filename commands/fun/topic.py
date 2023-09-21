# Credits for many of the response messages goes to the Lawliet Bot:
# https://github.com/Aninoss/lawliet-bot/tree/master/src/main/jib/data/resources

from discord import Embed, Color, ActionRow, Button, ButtonStyle

from utils import Command, Cooldowns

class CMD(Command):
  name = 'topic'
  cooldowns = Cooldowns(user=1e4)
  slash_command = True
  prefix_command = True
  dm_permission = True

  def run(self, msg, lang):
    embed = Embed(
        title=lang('embed_title'),
        description=lang('embed_description'),
        color=Color.random()
    ).set_footer(text=msg.user.username, icon_url=msg.user.display_avatar)

    component = ActionRow([Button(label=lang('global.anotherone'), custom_id='topic', style=ButtonStyle.primary)])

    return msg.custom_reply(embed=embed, components=[component])
