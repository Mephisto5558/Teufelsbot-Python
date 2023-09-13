from utils import Command, Option, Cooldowns, log_say_command_use

class CMD(Command):
  name = 'say'
  cooldowns = Cooldowns(user=200)
  slash_command = True
  prefix_command = True
  ephemeral_defer = False
  options = [
      Option(name='msg', type='String', max_length=2000, required=True),
      Option(name='channel', type='Channel', channel_types=TextBasedChannelTypes)
  ]

  def run(self, msg, lang):
    usr_msg:str = msg.content or msg.options.get_string('msg')
    channel = msg.options.get_channel('channel') or msg.mentions.channels.first() or msg.channel

    if PermissionFlagbits.SendMessages not in msg.member.permissions_in(channel):
      return msg.custom_reply(lang('no_perm'))
    if not usr_msg:
      return msg.custom_reply(lang('no_msg_provided'))

    allowed_mentions = {'parse': [AllowedMentionTypes.User], 'roles': [k for k, v in msg.guild.roles.cache.entries() if v.mentionable]}

    if PermissionFlagsBits.MentionEveryone in msg.member.permissions_in(channel):
      allowed_mentions['parse'].append(AllowedMentionTypes.Role)
      allowed_mentions['parse'].append(AllowedMentionTypes.Everyone)

    sent_message = channel.send(content=usr_msg.replace('/n', '\n'), allowed_mentions=allowed_mentions)
    msg.react('👍') if isinstance(msg, Message) else msg.custom_reply(lang('global.message_sent'))

    return log_say_command_use(sent_message, msg.member, lang)
    
