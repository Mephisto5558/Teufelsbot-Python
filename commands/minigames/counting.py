from discord import Embed, Color, ChannelType

from utils import Command, Option, Cooldowns, Permissions

class CMD(Command):
  name = 'counting'
  permissions = Permissions(user=['ManageChannels'])
  cooldowns = Cooldowns(user=1000)
  slash_command = True
  prefix_command = True
  options = [Option(name='channel', type='Channel', channel_types=ChannelType.TextBasedChannelTypes)]

  def run(self, msg, lang):
    channel = msg.options.get_channel('channel') or msg.mentions.channels.first() or msg.channel
    counting = msg.guild.db.counting or {}

    if counting[channel.id]:
      msg.client.db.delete('GUILD_SETTINGS', f'{msg.guild.id}.counting.{channel.id}')

      embed = Embed(description=lang('removed.embed_description'), color=Color.red()) \
          .set_footer(text=lang('removed.by', msg.user.name))

      if msg.channel.id == channel.id: return msg.custom_reply(embed=embed)

      channel.send(embed=embed)
      return msg.custom_reply(content=lang('removed.success', channel.id))

    embed = Embed(
        title=lang('added.embed_title'),
        description=lang('added.embed_description'),
        color=Color.green()
    ) .set_footer(text=lang('added.by', msg.user.name))

    msg.client.db.set('GUILD_SETTINGS', f'{msg.guild.id}.counting.{channel.id}', {'lastNumber': 0})

    if msg.channel.id == channel.id: return msg.custom_reply(embed=embed)
    channel.send(embed=embed)

    return msg.custom_reply(content=lang('added.success', channel.id))
