from utils import Aliases, Command, Option, Cooldowns, Permissions, Colors

class CMD(Command):
  name = 'nukechannel'
  aliases = Aliases(slash=['clearchannel'])
  permissions = Permissions(client=['ManageChannels'], user=['ManageGuild', 'ManageChannels'])
  cooldowns = Cooldowns(guild=1e4, user=1000)
  slash_command = True
  prefix_command = False
  options = [
      Option(name='confirmation', type='String', required=True),
      Option(name='channel', type='Channel', channel_types=Constants.TextBasedChannelTypes)
  ]

  def run(self, msg, lang):
    if msg.options.get_string('confirmation') != lang('confirmation'):
      return msg.edit_reply(lang('need_confirm'))

    embed = EmbedBuilder(
        description=lang('embed_description'),
        color=Colors.Red,
        image={'url': 'https://giphy.com/media/XUFPGrX5Zis6Y/giphy.gif'},
        footer={'text': lang('embed_footer_text', msg.user.tag)}
    )
    channel = msg.options.get_channel('channel') or msg.channel
    cloned = channel.clone(parent=channel.parent_id)

    channel.delete(lang('global.mod_reason', command=msg.command_name, user=msg.user.username))
    return cloned.send(embeds=[embed])
