# Credits for many of the response messages goes to the Lawliet Bot: https://github.com/Aninoss/lawliet-bot/tree/master/src/main/jib/data/resources

from utils import Command, Cooldowns

class CMD(Command):
  name = 'topic'
  cooldowns = Cooldowns(user=10000)
  slash_command = True
  prefix_command = True
  dm_permission = True

  def run(self, msg, lang):
    embed = EmbedBuilder(
        title=lang('embed_title'),
        description=lang('embed_description'),
        footer={'text': msg.user.tag, 'icon_url': msg.member.display_avatar_url()},
        color='Random'
    )
    component = ActionRowBuilder(components=[
        ButtonBuilder(label=lang('global.anotherone'), custom_id='topic', style=ButtonStyle.Primary)
    ])

    return msg.custom_reply(embeds=[embed], components=[component])
