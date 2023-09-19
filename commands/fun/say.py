from discord import ChannelType, AllowedMentions, Message

from utils import Command, Option, Cooldowns, log_say_command_use

class CMD(Command):
  name = 'say'
  cooldowns = Cooldowns(user=200)
  slash_command = True
  prefix_command = True
  ephemeral_defer = True
  options = [
      Option(name='msg', type='String', max_length=2000, required=True),
      Option(name='channel', type='Channel', channel_types=ChannelType.TextBasedChannelTypes)
  ]

  async def run(self, msg, lang):
    usr_msg: str = msg.content or msg.options.get_string('msg')
    channel = msg.options.get_channel('channel') or msg.mentions.channels.first() or msg.channel

    if not usr_msg:
      return msg.custom_reply(lang('no_msg_provided'))
    if not msg.user.resolved_permissions.send_messages:
      return msg.custom_reply(lang('no_perm'))

    sent_message = channel.send(
        content=usr_msg.replace('/n', '\n'),
        allowed_mentions=AllowedMentions(users=True, everyone=True, roles=True)
        if msg.user.resolved_permissions.mention_everyone
        else AllowedMentions(users=True)
    )

    if isinstance(msg, Message): await msg.add_reaction('👍')
    else: await msg.custom_reply(content=lang('global.message_sent'))

    return log_say_command_use(sent_message, msg.user, lang)
