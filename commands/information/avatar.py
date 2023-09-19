from discord import Embed, ActionRow, Button, ButtonStyle

from utils import Command, Option, Cooldowns

class CMD(Command):
  name = 'avatar'
  cooldowns = Cooldowns(guild=100, user=1000)
  slash_command = True
  prefix_command = True
  dm_permission = True
  options = [
      Option(name='target', type='User'),
      Option(
          name='size',
          type='Integer',
          choices=[16, 32, 56, 64, 96, 128, 256, 300, 512, 600, 1024, 2048]
      )
  ]

  def run(self, msg, lang):
    target = msg.options.get_member('target') or msg.mentions.members.first() or next((
        e for e in msg.guild.members
        if any(item in [e.id, e.user.name, e.user.tag, e.nick] for item in [*(msg.args or []), msg.content])
    ), None) or msg.user
    avatar_url = target.display_avatar_url(size=msg.options.get_integer('size') or 2048)
    embed = Embed(description=lang('embed_description', target.user.name), color=0) \
        .set_image(url=avatar_url)\
        .set_footer(url=msg.member.username)
    component = ActionRow(components=Button(label=lang('download_button'), url=avatar_url, style=ButtonStyle.link))

    return msg.custom_reply(embed=embed, components=[component])
