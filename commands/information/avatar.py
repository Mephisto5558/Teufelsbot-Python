from utils import Command, Option, Cooldowns, Colors

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
        e for e in msg.guild.members.cache
        if any(item in [e.user.id, e.user.username, e.user.tag, e.nickname] for item in [*(msg.args or []), msg.content])
    ), None) or msg.member
    avatar_url = target.display_avatar_url(size=msg.options.get_integer('size') or 2048)
    embed = EmbedBuilder(
        description=lang('embed_description', target.user.username),
        color=Colors.White,
        image={'url': avatar_url},
        footer={'text': msg.member.tag}
    )
    component = ActionRowBuilder(components=ButtonBuilder(label=lang('download_button'), url=avatar_url, style=ButtonStyle.Link))

    return msg.custom_reply(embeds=[embed], components=[component])
