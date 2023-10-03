from discord import ChannelType, Embed, Color

from utils import Command, Option, Cooldowns

class CMD(Command):
  name = 'lastping'
  cooldowns = Cooldowns(guild=200, user=1e4)
  slash_command = True
  prefix_command = True
  ephemeral_defer = False
  options = [
      Option(name='channel', type='Channel', channel_types=ChannelType.TextBasedChannelTypes),
      Option(name='member', type='User'),
      # Option(name='amount', type='Integer', min_value=0, max_value=20)
  ]

  def run(self, msg, lang):
    channel = msg.options.get_channel('channel') or msg.mentions.channels.first()
    target = msg.options.get_user('member') or msg.mentions.users.first()

    if target:
      if not channel: return msg.custom_reply(content=lang('member_requires_channel'))
      if not channel.isTextBased(): return msg.custom_reply(content=lang('invalid_channel'))

    if channel:
      message = next((e for e in channel.messages if (not target or e.author.id == target.id) and (
          e.mentions.everyone or msg.user.id in e.mentions.users
          or any(role in e.mentions.roles for role in msg.user.roles.keys())
      )), None)
    else:
      message = msg.guild.db[f'last_mentions.{msg.user.id}']

    if not message: return msg.custom_reply(content=lang('none_found'))

    embed = Embed(
        title=lang('embed_title'),
        description=lang(
            'embed_description',
            url=message.url,
            content=f'>>> {message.content[:200]}' if message.content else lang('unknown'),
            author=message.author.get('id') or message.author
        ),
        color=Color.white(),
        timestamp=message.created_at
    )

    return msg.response.edit_message(embeds=[embed])
