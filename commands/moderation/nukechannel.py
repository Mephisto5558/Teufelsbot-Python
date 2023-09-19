from discord import TextChannel, Interaction, Embed, Color, ChannelType

from utils import Aliases, Command, Option, Cooldowns, Permissions

class CMD(Command):
  name = 'nukechannel'
  aliases = Aliases(slash=['clearchannel'])
  permissions = Permissions(client=['ManageChannels'], user=['ManageGuild', 'ManageChannels'])
  cooldowns = Cooldowns(guild=1e4, user=1000)
  slash_command = True
  prefix_command = False
  options = [
      Option(name='confirmation', type='String', required=True),
      Option(name='channel', type='Channel', channel_types=ChannelType.TextBasedChannelTypes)
  ]

  async def run(self, msg: Interaction, lang):
    if msg.options.get_string('confirmation') != lang('confirmation'):
      return msg.response.edit_message(content=lang('need_confirm'))

    channel = msg.options.get_channel('channel') or msg.channel
    if not isinstance(channel, TextChannel): return  # type guard

    # todo: try catch
    cloned: TextChannel = await channel.clone(reason=lang('global.mod_reason', command=msg.command_name, user=msg.user.name))
    embed = Embed(description=lang('embed_description'), color=Color.red()) \
        .set_image(url='https://giphy.com/media/XUFPGrX5Zis6Y/giphy.gif')  \
        .set_footer(text=lang('embed_footer_text', msg.user.name))

    await channel.delete(reason=lang('global.mod_reason', command=msg.command_name, user=msg.user.name))
    return cloned.send(embeds=[embed])
